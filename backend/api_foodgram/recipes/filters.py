import django_filters as filters

from recipes.models import Ingredient, Recipe  # isort:skip

BOOLEAN_CHOICES = (
    (
        0,
        "false",
    ),
    (
        1,
        "true",
    ),
)


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
    is_favorited = filters.ChoiceFilter(
        choices=BOOLEAN_CHOICES,
        method="get_favorite",
        label="Favorited",
    )
    is_in_shopping_cart = filters.ChoiceFilter(
        choices=BOOLEAN_CHOICES,
        method="get_shopping",
        label="Is in shopping cart",
    )

    class Meta:
        model = Recipe
        fields = (
            "author",
            "tags",
        )

    def get_is_favorited(self, queryset, name, value):
        user = self.request.user
        value = int(value)
        if user.is_anonymous:
            return Recipe.objects.none() if value else queryset
        if value:
            return queryset.filter(favorite__user=user)
        return queryset.exclude(favorite__user=user)

    def get_is_in_shopping_cart(self, queryset, name, value):
        user = self.request.user
        value = int(value)
        if user.is_anonymous:
            return Recipe.objects.none() if value else queryset
        if value:
            return queryset.filter(shopping_cart__user=user)
        return queryset.exclude(shopping_cart__user=user)
