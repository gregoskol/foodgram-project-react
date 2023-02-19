from django.shortcuts import get_object_or_404
from rest_framework import mixins, status, viewsets
from rest_framework.decorators import action
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response

from .models import Follow, User
from .serializers import (
    FollowSerializer,
    PasswordChangeSerializer,
    RegistrationSerializer,
    UserSerializer,
)


class UserViewSet(
    mixins.CreateModelMixin,
    mixins.RetrieveModelMixin,
    mixins.ListModelMixin,
    viewsets.GenericViewSet,
):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [
        AllowAny,
    ]

    def create(self, request, *args, **kwargs):
        serializer = RegistrationSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(
            serializer.data, status=status.HTTP_201_CREATED, headers=headers
        )

    @action(
        detail=False, methods=["get"], permission_classes=(IsAuthenticated,)
    )
    def me(self, request):
        serializer = self.get_serializer(self.request.user)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @action(
        detail=False, methods=["post"], permission_classes=(IsAuthenticated,)
    )
    def set_password(self, request, pk=None):
        user = self.request.user
        serializer = PasswordChangeSerializer(data=request.data)
        if serializer.is_valid():
            if not user.check_password(
                serializer.data.get("current_password")
            ):
                return Response(
                    {"errors": "Текущий пароль указан неверно!"},
                    status=status.HTTP_400_BAD_REQUEST,
                )
            user.set_password(serializer.validated_data["new_password"])
            user.save()
            return Response(status=status.HTTP_204_NO_CONTENT)
        else:
            return Response(
                serializer.errors, status=status.HTTP_400_BAD_REQUEST
            )

    @action(
        methods=["post", "delete"],
        detail=True,
        url_path="subscribe",
        url_name="subscribe",
        permission_classes=[IsAuthenticated],
    )
    def subscribe(self, request, pk=None):
        user = request.user
        author = get_object_or_404(User, id=pk)
        if user == author:
            return Response(
                {"errors": "Нельзя подписаться на себя!"},
                status=status.HTTP_400_BAD_REQUEST,
            )
        subscription = Follow.objects.filter(author=author, user=user)
        if request.method == "POST":
            if subscription.exists():
                return Response(
                    {"errors": "Вы уже подписаны на этого автора"},
                    status=status.HTTP_400_BAD_REQUEST,
                )
            queryset = Follow.objects.create(author=author, user=user)
            serializer = FollowSerializer(
                queryset, context={"request": request}
            )
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        if request.method == "DELETE":
            if not subscription.exists():
                return Response(
                    {"errors": "Вы не были подписаны на этого автора"},
                    status=status.HTTP_400_BAD_REQUEST,
                )
            subscription.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)

    @action(
        detail=False, methods=["get"], permission_classes=(IsAuthenticated,)
    )
    def subscriptions(self, request):
        user = self.request.user
        users = User.objects.filter(following__user=user)
        serializer = FollowSerializer(users, many=True)
        page = self.paginate_queryset(users)
        if page is not None:
            return self.get_paginated_response(serializer.data)
        return Response(serializer.data)
