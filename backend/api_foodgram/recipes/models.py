from django.contrib.auth import get_user_model
from django.db import models

User = get_user_model()


class Ingredient(models.Model):
    name = models.CharField(max_length=200, verbose_name="Название")
    measurement_unit = models.CharField(
        max_length=200, verbose_name="Единица измерения"
    )

    class Meta:
        verbose_name = "Ингредиент"
        verbose_name_plural = "Ингредиенты"

    def __str__(self):
        return self.name


class Tag(models.Model):
    name = models.CharField(
        max_length=200, unique=True, verbose_name="Название"
    )
    color = models.CharField(
        max_length=7, unique=True, verbose_name="Цвет в HEX"
    )
    slug = models.SlugField(max_length=200, unique=True, verbose_name="Слаг")

    class Meta:
        verbose_name = "Тег"
        verbose_name_plural = "Теги"

    def __str__(self):
        return self.name


class Recipe(models.Model):
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="recipes",
        verbose_name="Автор",
    )
    ingredients = models.ManyToManyField(
        Ingredient, through="IngredientRecipe", verbose_name="Ингредиенты"
    )
    tags = models.ManyToManyField(Tag, through="TagRecipe")
    image = models.ImageField(
        upload_to="recipes/images/",
        null=True,
        default=None,
        verbose_name="Картинка",
    )
    name = models.CharField(max_length=200, verbose_name="Название")
    text = models.TextField(verbose_name="Описание")
    cooking_time = models.IntegerField(
        verbose_name="Время приготовления (в минутах)"
    )

    class Meta:
        ordering = ("-id",)
        verbose_name = "Рецепт"
        verbose_name_plural = "Рецепты"

    def __str__(self):
        return self.name


class TagRecipe(models.Model):
    tag = models.ForeignKey(Tag, on_delete=models.CASCADE, verbose_name="Тег")
    recipe = models.ForeignKey(
        Recipe, on_delete=models.CASCADE, verbose_name="Рецепт"
    )

    class Meta:
        verbose_name = "Пара тег-рецепт"
        verbose_name_plural = "Пары тег-рецепт"
        constraints = [
            models.UniqueConstraint(
                fields=["tag", "recipe"], name="unique_tag_recipe"
            )
        ]

    def __str__(self):
        return f"{self.tag} {self.recipe}"


class IngredientRecipe(models.Model):
    ingredient = models.ForeignKey(
        Ingredient, on_delete=models.PROTECT, verbose_name="Ингредиент"
    )
    recipe = models.ForeignKey(
        Recipe, on_delete=models.CASCADE, verbose_name="Рецепт"
    )
    amount = models.PositiveIntegerField(verbose_name="Количество")

    class Meta:
        verbose_name = "Пара ингредиент-рецепт"
        verbose_name_plural = "Пары ингредиент-рецепт"
        constraints = [
            models.UniqueConstraint(
                fields=["ingredient", "recipe"],
                name="unique_ingredient_recipe",
            )
        ]

    def __str__(self):
        return f"{self.ingredient} {self.recipe}"


class Favorite(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="favorite",
        verbose_name="Автор",
    )
    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        related_name="favorite",
        verbose_name="Рецепт",
    )

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["user", "recipe"],
                name="unique_recipe_in_user_favorite",
            )
        ]
        verbose_name = "Избранное"
        verbose_name_plural = "Избранное"


class ShoppingCart(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="shopping_cart",
        verbose_name="Пользователь",
    )
    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        related_name="shopping_cart",
        verbose_name="Рецепт",
    )

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["user", "recipe"], name="unique_shopping_cart"
            )
        ]
        verbose_name = "Список покупок"
        verbose_name_plural = "Списки покупок"
