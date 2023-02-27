from django.urls import path
from . import views

urlpatterns = [
    path("", views.home, name="home"),
    path("about/", views.about, name="about"),
    path("academy/", views.academy, name="academy"),
    path("life-events/", views.live_event, name="live_event"),
    path("plans/", views.plans, name="plans"),
    path("contact/", views.contact, name="contact"),
    path("index.html/", views.indexh, name="indexh"),
]
