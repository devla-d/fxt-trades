from django.urls import path
from . import views

urlpatterns = [
    path("register/", views.reg_ister, name="register"),
    path("login/", views.log_in, name="login"),
    path("sign-out/", views.sign_out, name="sign_out"),
]
