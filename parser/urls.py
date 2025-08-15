from django.urls import path

from parser import views

urlpatterns = [
    path("", views.PayStrParser.as_view(), name="paystr"),
]

app_name = "parser"
