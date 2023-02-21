from django.contrib.auth.models import AbstractUser
from django.db import models
from django.db.models import CheckConstraint, UniqueConstraint


class User(AbstractUser):
    email = models.EmailField(
        max_length=254, unique=True, verbose_name="Электронная почта"
    )
    username = models.CharField(
        max_length=150, blank=False, unique=True, verbose_name="Логин"
    )
    first_name = models.CharField(
        max_length=150, blank=False, verbose_name="Имя"
    )
    last_name = models.CharField(
        max_length=150, blank=False, verbose_name="Фамилия"
    )

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["username", "first_name", "last_name"]

    class Meta:
        ordering = ["username"]
        verbose_name = "Пользователь"
        verbose_name_plural = "Пользователи"

    def __str__(self):
        return self.username


class Follow(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="user",
        verbose_name="Подписчик",
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="following",
        verbose_name="Автор",
    )

    class Meta:
        constraints = [
            UniqueConstraint(fields=["user", "author"], name="unique_follow"),
            CheckConstraint(
                check=~models.Q(user=models.F("author")),
                name="no_follow_myself",
            ),
        ]
        verbose_name = "Подписка"
        verbose_name_plural = "Подписки"

    def __str__(self):
        return f"{self.user} подписан на {self.author}"
