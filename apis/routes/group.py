from django.urls import path
from ..views.group import CreateGroup, ListGroup

urlpatterns = [path("", ListGroup.as_view()), path("create/", CreateGroup.as_view())]
