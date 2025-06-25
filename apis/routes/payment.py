from django.urls import path
from ..views.payment import CreatePayment, ListPayment, DeletePayment

urlpatterns = [
    path("create/<int:groupMemberId>/", CreatePayment.as_view()),
    path("delete/<int:payment_id>/", DeletePayment.as_view()),
    path("", ListPayment.as_view()),
]
