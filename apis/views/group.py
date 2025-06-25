from rest_framework import generics
from ..serializers import GroupSerializer
from ..models import Group
from rest_framework.permissions import IsAuthenticated


class CreateGroup(generics.CreateAPIView):
    serializer_class = GroupSerializer
    model = Group
    permission_classes = [IsAuthenticated]


class ListGroup(generics.ListAPIView):
    serializer_class = GroupSerializer
    model = Group
    queryset = Group.objects.all()
