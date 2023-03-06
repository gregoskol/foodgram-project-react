from django.contrib import admin

from .models import (  # isort: skip
    Favorite,
    Ingredient,
    IngredientRecipe,
    Recipe,
    ShoppingCart,
    Tag,
    TagRecipe,
)


class IngredientInline(admin.TabularInline):
    model = IngredientRecipe


class TagInline(admin.TabularInline):
    model = TagRecipe


@admin.register(Ingredient)
class IngredientAdmin(admin.ModelAdmin):
    list_display = (
        "pk",
        "name",
        "measurement_unit",
    )
    list_filter = ("name",)
    empty_value_display = "-пусто-"


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = (
        "pk",
        "name",
        "color",
        "slug",
    )
    list_filter = ("name",)
    empty_value_display = "-пусто-"


@admin.register(Recipe)
class RecipeAdmin(admin.ModelAdmin):
    list_display = ("pk", "name", "author", "in_favorite")
    list_filter = ("name", "author", "tags")
    readonly_fields = ("in_favorite",)
    empty_value_display = "-пусто-"
    inlines = [
        IngredientInline,
        TagInline,
    ]

    def in_favorite(self, obj):
        return obj.favorite.all().count()

    in_favorite.short_description = "В избранном"


@admin.register(Favorite)
class AdminFavorite(admin.ModelAdmin):
    list_display = ("pk", "user", "recipe")


@admin.register(ShoppingCart)
class AdminShoppingCart(admin.ModelAdmin):
    list_display = ("pk", "user", "recipe")


@admin.register(IngredientRecipe)
class IngredientRecipeAdmin(admin.ModelAdmin):
    list_display = (
        "pk",
        "ingredient",
        "recipe",
    )

    empty_value_display = "-пусто-"


@admin.register(TagRecipe)
class TagRecipeAdmin(admin.ModelAdmin):
    list_display = (
        "pk",
        "tag",
        "recipe",
    )

    empty_value_display = "-пусто-"
