import django_filters as filters

from recipes.models import Ingredient, Recipe, Tag  # isort:skip
from users.models import User  # isort:skip


class IngredientsFilter(filters.FilterSet):
    name = filters.CharFilter(
        field_name="name",
        lookup_expr="icontains",
    )

    class Meta:
        model = Ingredient
        fields = ("name",)


class RecipeFilter(filters.FilterSet):
    tags = filters.AllValuesMultipleFilter(
        field_name="tags__slug",
        lookup_expr="iexact",
        label="Tags",
    )
    is_favorited = filters.BooleanFilter(
        method="get_favorite",
        label="Favorited",
    )
    is_in_shopping_cart = filters.BooleanFilter(
        method="get_shopping",
        label="Is in shopping list",
    )

    class Meta:
        model = Recipe
        fields = (
            "is_favorited",
            "author",
            "tags",
            "is_in_shopping_cart",
        )

    def get_favorite(self, queryset, name, item_value):
        if self.request.user.is_authenticated and item_value:
            return queryset.filter(favorite__user=self.request.user)

    def get_shopping(self, queryset, name, item_value):
        if self.request.user.is_authenticated and item_value:
            return queryset.filter(shopping_cart__user=self.request.user)
