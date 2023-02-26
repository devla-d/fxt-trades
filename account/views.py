from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate
from django.contrib import messages

from django.contrib.auth.tokens import default_token_generator
from django.contrib.sites.shortcuts import get_current_site
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode
from django.core.mail import EmailMessage
from django.template.loader import get_template


from baseapp import utils
from .forms import RegisterForm, LoginForm
from .models import Account, LoginHistory, Referral


def reg_ister(request):
    if request.GET.get("ref-code"):
        ref_code = request.GET.get("ref-code")
    else:
        ref_code = None
    if request.GET.get("act"):
        act = request.GET.get("act")
    else:
        act = None
    if request.POST:
        form = RegisterForm(request.POST)
        if form.is_valid():
            instance = form.save(commit=False)
            instance.is_active = True
            instance.unique_id = utils.reg_code()
            instance.save()

            if ref_code != None:
                try:
                    old_user = Account.objects.get(unique_id=ref_code)
                except Account.DoesNotExist:
                    messages.warning(request, ("UNKNOWN ERROR OCCURED !"))
                    return redirect("register")
                old_user_ref_model = Referral.objects.get(user=old_user)
                new_user_ref_model, created = Referral.objects.get_or_create(
                    user=instance, referred_by=old_user
                )

                old_user.referral_bonus += 10
                old_user.balance += 10
                old_user.referral += 1
                old_user.save()

                old_user_ref_model.referrals.add(instance)

                new_user_ref_model.referred_by = old_user
            else:
                Referral.objects.create(user=instance)

            current_site = get_current_site(request)
            subject = f"Welcome to {current_site.domain}"
            context = {
                "user": instance,
                "domain": current_site.domain,
                "uid": urlsafe_base64_encode(force_bytes(instance.pk)),
                "token": default_token_generator.make_token(instance),
            }
            message = get_template("auth/welcomEmail.html").render(context)
            mail = EmailMessage(
                subject=subject,
                body=message,
                from_email=utils.EMAIL_ADMIN,
                to=[instance.email],
                reply_to=[utils.EMAIL_ADMIN],
            )
            mail.content_subtype = "html"
            mail.send(fail_silently=True)
            messages.info(request, "Account created")

            return redirect("login")
    else:
        form = RegisterForm()
    return render(
        request, "auth/register.html", {"ref_code": ref_code, "form": form, "act": act}
    )


def log_in(request):
    destination = utils.get_next_destination(request)
    if request.POST:
        form = LoginForm(request.POST)
        if form.is_valid():
            user = authenticate(
                email=form.cleaned_data["email"], password=form.cleaned_data["password"]
            )
            if user:
                login(request, user)
                LoginHistory.objects.create(
                    user=user, log_ip=utils.get_client_ip(request), city="####"
                )
                if destination:
                    return redirect(f"{destination}")
                else:
                    return redirect("dashboard")
        else:
            messages.warning(request, ("Invalid Username Or Password."))
            return redirect("login")
    else:
        form = LoginForm()
    return render(request, "auth/login.html", {"form": form})


def sign_out(request):
    logout(request)
    return redirect("login")
