from django.urls import path
from ..views.member import CreateMemberByGroupId

urlpatterns = [path("create/<int:groupId>/", CreateMemberByGroupId.as_view())]
