from django_filters import ModelMultipleChoiceFilter
from django_filters.rest_framework import FilterSet, filters

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


class TagFilter(FilterSet):
    tags = ModelMultipleChoiceFilter(
        field_name="tags__slug",
        to_field_name="slug",
        queryset=Tag.objects.all(),
    )
    author = filters.ModelChoiceFilter(queryset=User.objects.all())
    is_favorited = filters.BooleanFilter(method="filter_favorite")
    is_in_shopping_cart = filters.BooleanFilter(method="filter_shopping_cart")

    def filter_favorite(self, queryset, name, value):
        if value:
            return queryset.filter(favorite__user=self.request.user)
        return queryset

    def filter_shopping_cart(self, queryset, name, value):
        if value:
            return queryset.filter(shopping_cart__user=self.request.user)
        return queryset

    class Meta:
        model = Recipe
        fields = ("tags", "author")
