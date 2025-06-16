from rest_framework import generics
from ..serializers import GroupSerializer
from ..models import Group


class CreateGroup(generics.CreateAPIView):
    serializer_class = GroupSerializer
    model = Group


class ListGroup(generics.ListAPIView):
    serializer_class = GroupSerializer
    model = Group
    queryset = Group.objects.all()
