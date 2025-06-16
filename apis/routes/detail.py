from django.urls import path
from ..views.detail import get_user_groups_data

urlpatterns = [path("<int:user_id>/", get_user_groups_data)]
