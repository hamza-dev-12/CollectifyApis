from rest_framework import generics
from ..serializers import MemberSerializer
from ..models import Member, Group


class CreateMemberByGroupId(generics.CreateAPIView):
    serializer_class = MemberSerializer
    model = Member

    def perform_create(self, serializer):
        if serializer.is_valid():
            group = Group.objects.get(pk=self.kwargs.get("groupId"))
            serializer.save(group=group)


class ListMembersById(generics.ListAPIView):
    def get_queryset(self):
        return Member.objects.get(group=self.kwargs.get("groupId"))
