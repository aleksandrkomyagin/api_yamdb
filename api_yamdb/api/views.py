from django.contrib.auth import get_user_model
from django.db.models import Avg
from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters, permissions, status
from rest_framework.decorators import action, api_view, permission_classes
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import AccessToken

from api.filters import TitleFilter
from api.permissions import (IsAdminOrReadOnly, IsAdminUser,
                             IsAuthorModeratorAdminOrReadOnly)
from api.serializers import (CategorySerializer, CommentSerializer,
                             GenreSerializer, GetTitleSerializer,
                             MeUserSerializer, PostTitleSerializer,
                             ReviewSerializer, UserConfirmationCodeSerializer,
                             UserSerializer, UserTokenSerializer)
from api.utils import GenreCategoryViewSet, ViewSetWithoutPut
from reviews.models import Category, Genre, Review, Title

User = get_user_model()


@api_view(['POST'])
@permission_classes([permissions.AllowAny])
def get_confirmation_code(request):
    serializers = UserConfirmationCodeSerializer(data=request.data)
    serializers.is_valid(raise_exception=True)
    username = serializers.validated_data.get('username')
    email = serializers.validated_data.get('email')
    user_by_username = User.objects.filter(username=username).first()
    user_by_email = User.objects.filter(email=email).first()
    if user_by_username != user_by_email:
        field_name = 'username' if user_by_username else 'email'
        return Response(
            {"Ошибка": f"Пользователь с введенным {field_name} существует!"},
            status=status.HTTP_400_BAD_REQUEST)
    target_user, _ = User.objects.get_or_create(username=username, email=email)
    target_user.send_mail
    return Response(serializers.data)


@api_view(['POST'])
@permission_classes([permissions.AllowAny])
def get_token_view(request):
    serializer = UserTokenSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    username = serializer.validated_data.get('username')
    user = get_object_or_404(User, username=username)
    code = user.confirmation_code
    if serializer.validated_data.get('confirmation_code') == str(code):
        token = AccessToken.for_user(user)
        return Response({'token': str(token)},
                        status=status.HTTP_200_OK)
    return Response(
        {'confirmation_code': 'Неверный код подтверждения!'},
        status=status.HTTP_400_BAD_REQUEST)


class UserViewSet(ViewSetWithoutPut):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = (IsAdminUser, permissions.IsAuthenticated)
    lookup_field = 'username'
    filter_backends = (filters.SearchFilter, )
    search_fields = ('username', )

    @action(
        methods=['GET', 'PATCH'],
        permission_classes=(permissions.IsAuthenticated,),
        detail=False,
        url_path='me'
    )
    def get_update_user(self, request):
        serializer = UserSerializer(request.user)
        if request.method == 'PATCH':
            serializer = MeUserSerializer(
                request.user,
                data=request.data,
                partial=True)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.data)


class CategoryViewSet(GenreCategoryViewSet):
    """Операции связананные с категориями"""
    queryset = Category.objects.all()
    serializer_class = CategorySerializer


class GenreViewSet(GenreCategoryViewSet):
    """Операции связананные с жанрами"""
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer


class TitleViewSet(ViewSetWithoutPut):
    """Операции связананные с названиями произведений"""
    queryset = Title.objects.all().annotate(
        rating=Avg('reviews_title__score')).order_by('name')
    permission_classes = (IsAdminOrReadOnly,)
    filter_backends = (DjangoFilterBackend,)
    filterset_class = TitleFilter

    def get_serializer_class(self):
        if self.request.method in ('POST', 'PATCH',):
            return PostTitleSerializer
        return GetTitleSerializer


class ReviewViewSet(ViewSetWithoutPut):
    permission_classes = (IsAuthorModeratorAdminOrReadOnly,)
    serializer_class = ReviewSerializer

    def get_title(self):
        title_id = self.kwargs.get('title_id')

        return get_object_or_404(Title, pk=title_id)

    def get_queryset(self):
        title = self.get_title()

        return title.reviews_title.all()

    def perform_create(self, serializer):
        serializer.save(author=self.request.user, title=self.get_title())


class CommentViewSet(ViewSetWithoutPut):
    permission_classes = (IsAuthorModeratorAdminOrReadOnly,)
    serializer_class = CommentSerializer

    def get_queryset(self):
        review = get_object_or_404(
            Review,
            pk=self.kwargs.get('review_id'),
            title=self.kwargs.get('title_id')
        )
        return review.comment_review.all()

    def perform_create(self, serializer):
        review = get_object_or_404(
            Review,
            pk=self.kwargs.get('review_id'),
            title=self.kwargs.get('title_id')
        )
        serializer.save(
            author=self.request.user,
            review=review
        )
