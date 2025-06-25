from rest_framework import generics
from ..serializers import MemberSerializer
from ..models import Member, Group
from rest_framework.permissions import IsAuthenticated


class CreateMemberByGroupId(generics.CreateAPIView):
    serializer_class = MemberSerializer
    model = Member
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        if serializer.is_valid():
            group = Group.objects.get(pk=self.kwargs.get("groupId"))
            serializer.save(group=group)


class ListMembersById(generics.ListAPIView):
    def get_queryset(self):
        return Member.objects.get(group=self.kwargs.get("groupId"))


class DeleteMemberById(generics.DestroyAPIView):
    queryset = Member.objects.all()
    serializer_class = MemberSerializer
    model = Member
    lookup_field = "pk"
    lookup_url_kwarg = "member_id"
