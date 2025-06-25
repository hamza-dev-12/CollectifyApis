from django.urls import path
from ..views.chat import chat

urlpatterns = [path("<int:group_id>/", chat)]
