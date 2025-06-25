from django.urls import path
from ..views.users import CreateUser, ListUser, Login, DeleteUser

urlpatterns = [
    path("", ListUser.as_view()),
    path("signup/", CreateUser.as_view()),
    path("login/", Login.as_view()),
    path("delete/<int:user_id>/", DeleteUser.as_view()),
]
