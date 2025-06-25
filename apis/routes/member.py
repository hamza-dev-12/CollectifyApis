from django.urls import path
from ..views.member import CreateMemberByGroupId, DeleteMemberById

urlpatterns = [
    path("create/<int:groupId>/", CreateMemberByGroupId.as_view()),
    path("delete/<int:member_id>/", DeleteMemberById.as_view()),
]
