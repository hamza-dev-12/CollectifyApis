from django.urls import path
from ..views.payment import CreatePayment, ListPayment

urlpatterns = [
    path("create/<int:groupMemberId>/", CreatePayment.as_view()),
    path("", ListPayment.as_view()),
]
