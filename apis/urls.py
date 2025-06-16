from django.urls import path, include

urlpatterns = [
    path("user/", include("apis.routes.user")),
    path("group/", include("apis.routes.group")),
    path("member/", include("apis.routes.member")),
    path("payment/", include("apis.routes.payment")),
    path("detail/", include("apis.routes.detail")),
]
