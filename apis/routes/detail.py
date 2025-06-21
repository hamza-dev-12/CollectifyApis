from django.urls import path
from ..views.detail import get_user_groups_data, get_group_detail_by_id

urlpatterns = [
    path("<int:user_id>/", get_user_groups_data),
    path("group/<int:group_id>/", get_group_detail_by_id),
]
