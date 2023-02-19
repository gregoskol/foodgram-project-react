from django.urls import include, path
from djoser.views import TokenCreateView, TokenDestroyView
from rest_framework import routers

from .views import UserViewSet

router = routers.DefaultRouter()
router.register("users", UserViewSet)
urlpatterns = [
    path("auth/token/login/", TokenCreateView.as_view()),
    path("auth/token/logout/", TokenDestroyView.as_view()),
    path("", include(router.urls)),
]
