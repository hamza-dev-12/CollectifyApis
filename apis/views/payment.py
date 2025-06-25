from rest_framework import generics
from ..models import Payment, Member
from ..serializers import PaymentSerializer
from rest_framework.permissions import IsAuthenticated


class CreatePayment(generics.CreateAPIView):
    model = Payment
    serializer_class = PaymentSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        print(serializer)
        if serializer.is_valid():
            print(serializer)
            member = Member.objects.get(id=self.kwargs.get("groupMemberId"))
            print(member)
            if serializer.is_valid():
                serializer.save(status="paid", group_members=member)


class ListPayment(generics.ListAPIView):
    model = Payment
    serializer_class = PaymentSerializer

    def get_queryset(self):
        payments = Payment.objects.select_related("group_members").all()
        groupId = self.request.query_params.get("groupId")
        month = self.request.query_params.get("month")

        if groupId:
            filter_kwargs = {"group_members__group": groupId}
            payments = payments.filter(**filter_kwargs)

        if month:
            filter_kwargs = {"date__month": month}
            payments = payments.filter(**filter_kwargs)

        return payments


class DeletePayment(generics.DestroyAPIView):
    serializer_class = PaymentSerializer
    model = Payment
    queryset = Payment.objects.all()
    permission_classes = [IsAuthenticated]
    lookup_field = "pk"
    lookup_url_kwarg = "payment_id"
