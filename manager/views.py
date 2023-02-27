from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import get_user_model
from django.core.mail import EmailMessage
from django.template.loader import get_template
from django.contrib import messages
from django.contrib.sites.shortcuts import get_current_site
from django.contrib.auth import login, logout
from user.models import Transactions, Investments

from baseapp import utils
from .decorator import manager_required

Account = get_user_model()


@manager_required
def dashboard(request):
    total_earnings = 0
    investments = Investments.objects.all()
    for invest in investments:
        total_earnings += invest.amount_invested
    am_deposit = 0
    am_withdraw = 0
    for obj in Transactions.objects.all():
        if obj.trans_type == utils.D:
            am_deposit += obj.amount
        elif obj.trans_type == utils.W:
            am_withdraw += obj.amount

    context = {
        "earnings": total_earnings,
        "am_deposit": am_deposit,
        "am_withdraw": am_withdraw,
        "users": Account.objects.all().count(),
        "withdrawal": Transactions.objects.filter(trans_type=utils.W).count(),
        "deposit": Transactions.objects.filter(trans_type=utils.D).count(),
        "withdrawal_pending": Transactions.objects.filter(
            trans_type=utils.W, status="pending"
        ).count(),
        "deposit_pending": Transactions.objects.filter(
            trans_type=utils.D, status="pending"
        ).count(),
    }
    return render(request, "superadmin/dashboard.html", context)


@manager_required
def users(request):
    users = Account.objects.all()
    return render(request, "superadmin/users.html", {"users": users})


@manager_required
def user_detail(request, pk):
    try:
        account = Account.objects.get(pk=pk)
        try:
            investment = Investments.objects.get(user=account)

        except:
            investment = None
    except Account.DoesNotExist:
        account = None
    # try:
    #     investment  = Investments.objects.filter(user=account)
    # except
    # print(investment.user)
    if request.POST:
        amount = int(request.POST.get("amount"))
        submit = request.POST.get("submit")
        if submit == "Submit":
            transaction = Transactions.objects.create(
                user=account,
                amount=amount,
                trans_type=utils.D,
                status="approved",
                unique_u=utils.trans_code(),
            )
            account.deposit_balance += amount
            account.save()
            utils.create_notification(
                user=account,
                title="Account Deposited",
                body=f"Your Account has been deposited with the sum of ${amount}",
            )

            current_site = get_current_site(request)
            subject = "Account Deposited"
            context = {
                "user": account,
                "domain": current_site.domain,
                "amount": amount,
                "transaction": transaction,
            }
            message = get_template("superadmin/deposit_email.html").render(context)
            mail = EmailMessage(
                subject=subject,
                body=message,
                from_email=utils.EMAIL_ADMIN,
                to=[account.email],
                reply_to=[utils.EMAIL_ADMIN],
            )
            mail.content_subtype = "html"
            mail.send(fail_silently=True)

            messages.success(request, "Account Deposit Successful")
            return redirect("user_detail", pk=account.id)

        elif submit == "Top up":
            account.balance += amount
            account.save()
            utils.create_notification(
                user=account,
                title="Account Balance Top up",
                body=f"Your account balance has been credited with the sum of ${amount}",
            )
            messages.success(request, "Account Top Up Successful")
            return redirect("user_detail", pk=account.id)
        else:
            messages.warning(request, "UNKNOWN ERROR OCCURED")
            return redirect("user_detail", pk=account.id)

    return render(
        request,
        "superadmin/user_detail.html",
        {"account": account, "investment": investment},
    )


@manager_required
def withdrawal_(request):
    """
    LIST ALL WITHDRAWAL
    """
    transactions = Transactions.objects.filter(trans_type=utils.W).order_by("-date")
    return render(request, "superadmin/withdrawal.html", {"transactions": transactions})


@manager_required
def withdrawal_detail(request, pk):
    """
    GET DETAILS OF A  WITHDRAWAL
    """
    try:
        transaction = Transactions.objects.get(pk=pk)
    except Transactions.DoesNotExist:
        transaction = None
        return redirect("withdrawal_")
    if request.POST:
        submit = request.POST.get("submit")
        if submit == "decline":
            transaction.status = "declined"
            transaction.save()

            current_site = get_current_site(request)
            subject = "Withdrawal Declined"
            context = {
                "status": "declined",
                "domain": current_site.domain,
                "transaction": transaction,
            }
            message = get_template("superadmin/withdraw_email.html").render(context)
            mail = EmailMessage(
                subject=subject,
                body=message,
                from_email=utils.EMAIL_ADMIN,
                to=[transaction.user.email],
                reply_to=[utils.EMAIL_ADMIN],
            )
            mail.content_subtype = "html"
            mail.send(fail_silently=True)
            utils.create_notification(
                user=transaction.user,
                title="Investment Credited",
                body=f"Your withdrawal of  ${transaction.amount}  has been declined",
            )

            messages.warning(request, "Withdrawal declined")
            return redirect("withdrawal_detail", pk=transaction.pk)

        elif submit == "approve":
            transaction.status = "approved"
            transaction.user.total_withdraw += transaction.amount
            transaction.user.save()
            transaction.save()

            current_site = get_current_site(request)
            subject = "Withdrawal Approved"
            context = {
                "status": "approved",
                "domain": current_site.domain,
                "transaction": transaction,
            }
            message = get_template("superadmin/withdraw_email.html").render(context)
            mail = EmailMessage(
                subject=subject,
                body=message,
                from_email=utils.EMAIL_ADMIN,
                to=[transaction.user.email],
                reply_to=[utils.EMAIL_ADMIN],
            )
            mail.content_subtype = "html"
            mail.send(fail_silently=True)
            utils.create_notification(
                user=transaction.user,
                title="Investment Credited",
                body=f"Your withdrawal of  ${transaction.amount}  has been Approved",
            )

            messages.success(request, "Withdrawal Approved")
            return redirect("withdrawal_detail", pk=transaction.pk)

        else:
            messages.success(request, "UNKNOWN ERROR OCCURED")
            return redirect("withdrawal_detail", pk=transaction.pk)

    return render(
        request, "superadmin/withdrawal_detail.html", {"transaction": transaction}
    )


@manager_required
def deposit_(request):
    """
    LIST ALL DEPOSIT
    """
    transactions = Transactions.objects.filter(trans_type=utils.D).order_by("-date")
    return render(request, "superadmin/deposit.html", {"transactions": transactions})


def login_user_account(request, pk):
    """
    LOG IN USER ACCOUNT
    """
    logout(request)
    user = Account.objects.get(pk=pk)
    login(request, user)
    messages.success(request, f"Logged In As {user.username}")
    return redirect("dashboard")


@manager_required
def investments(request):
    """
    GET LIST OF A  INVESTMENTS
    """
    investments = Investments.objects.all().order_by("-date")
    return render(request, "superadmin/investments.html", {"investments": investments})


@manager_required
def investments_detail(request, pk):
    """
    GET DETAILS OF A  INVESTMENTS
    """
    try:
        investment = Investments.objects.get(pk=pk)
    except Investments.DoesNotExist:
        investment = None
        messages.success(request, f"UNKNOW ERROR OCCURED")
        return redirect("investments")
    if request.POST:
        if investment.status != "completed":
            # investment.user.balance += investment.amount_earn
            investment.status = "completed"
            # investment.user.save()
            investment.save()
            utils.create_notification(
                user=investment.user,
                title="Investment Completed",
                body=f"Your investment have just been completed",
            )
        messages.success(request, f"Investment completed")
        return redirect("investments_detail", pk=pk)

    else:
        return render(
            request, "superadmin/investment_detail.html", {"investment": investment}
        )


@manager_required
def investments_topup(request):
    if request.POST:
        invest_pk = request.POST.get("invest_id")
        amount = int(request.POST.get("amount"))

        investment = get_object_or_404(Investments, pk=invest_pk)

        investment.amount_earn += amount
        investment.save()
        utils.create_notification(
            user=investment.user,
            title="Investment Credited",
            body=f"You just earned ${amount} from your investment",
        )
        messages.info(request, "Toped up successfull")
        return redirect("investments_detail", pk=invest_pk)
    else:
        messages.info(request, "Not Found")
        return redirect("investments")


@manager_required
def send_message(request):
    if request.POST:
        title = request.POST.get("title")
        rname = request.POST.get("rname")
        email = request.POST.get("remail")
        rmessage = request.POST.get("rmessage")

        context = {
            "name": rname,
            "body": rmessage,
        }
        message = get_template("superadmin/mail_temp.html").render(context)
        mail = EmailMessage(
            subject=title,
            body=message,
            from_email=utils.EMAIL_ADMIN,
            to=[email],
            reply_to=[utils.EMAIL_ADMIN],
        )
        mail.content_subtype = "html"
        mail.send(fail_silently=True)

        messages.info(request, "Mail Sent")
        return redirect("send_message")

    return render(request, "superadmin/send_email.html")
