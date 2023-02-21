from django.urls import include, path
from djoser.views import TokenCreateView, TokenDestroyView
from rest_framework import routers

from recipes.views import (
    IngredientViewSet,
    RecipeViewSet,
    TagViewSet,
)  # isort: skip
from users.views import UserViewSet  # isort: skip

router_v1 = routers.DefaultRouter()
router_v1.register("users", UserViewSet)
router_v1.register("tags", TagViewSet)
router_v1.register("ingredients", IngredientViewSet)
router_v1.register("recipes", RecipeViewSet)
urlpatterns = [
    path("auth/token/login/", TokenCreateView.as_view()),
    path("auth/token/logout/", TokenDestroyView.as_view()),
    path("", include(router_v1.urls)),
]
