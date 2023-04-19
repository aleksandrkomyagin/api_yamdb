from django.contrib.auth import get_user_model
from django.db.models import Avg
from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters, permissions, status, viewsets
from rest_framework.decorators import action, api_view, permission_classes
from rest_framework.exceptions import MethodNotAllowed
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import AccessToken
from reviews.models import Category, Genre, Review, Title

from .filters import TitleFilter
from .mixins import CreateListDeleteViewSet
from api.permissions import (IsAdminOrReadOnly, IsAdminUser,
                             IsAuthorModeratorAdminOrReadOnly)
from api.serializers import (CategorySerializer, CommentSerializer,
                             GenreSerializer, GetTitleSerializer,
                             NotAdminSerializer, PostTitleSerializer,
                             ReviewSerializer, UserConfirmationCodeSerializer,
                             UserSerializer, UserTokenSerializer)

User = get_user_model()


@api_view(['POST'])
@permission_classes([permissions.AllowAny])
def get_confirmation_code(request):
    serializers = UserConfirmationCodeSerializer(data=request.data)
    serializers.is_valid(raise_exception=True)
    username = serializers.validated_data.get('username')
    email = serializers.validated_data.get('email')
    target_user = User.objects.filter(username=username, email=email).first()
    if target_user:
        target_user.send_mail
        return Response(serializers.data)
    else:
        user_by_username = User.objects.filter(username=username)
        user_by_email = User.objects.filter(email=email)
        if user_by_username:
            return Response(
                {"Ошибка": "Пользователь с введенным username существует!"},
                status=status.HTTP_400_BAD_REQUEST)
        if user_by_email:
            return Response(
                {"Ошибка": "Пользователь с введенным email существует!"},
                status=status.HTTP_400_BAD_REQUEST)
    user = User.objects.create(username=username, email=email)
    user.send_mail
    return Response(serializers.data)


@api_view(['POST'])
@permission_classes([permissions.AllowAny])
def get_token_view(request):
    serializer = UserTokenSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    username = serializer.validated_data.get('username')
    user = User.objects.filter(username=username).first()
    if not user:
        return Response(
            {"Ошибка": "Нет пользователь с таким username"},
            status=status.HTTP_404_NOT_FOUND)
    code = user.confirmation_code
    if serializer.validated_data.get('confirmation_code') == str(code):
        token = AccessToken.for_user(user)
        return Response({'token': str(token)},
                        status=status.HTTP_200_OK)
    return Response(
        {'confirmation_code': 'Неверный код подтверждения!'},
        status=status.HTTP_400_BAD_REQUEST)


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = (IsAdminUser, permissions.IsAuthenticated)
    lookup_field = 'username'
    filter_backends = (filters.SearchFilter, )
    search_fields = ('username', )
    http_method_names = ['get', 'post', 'patch', 'delete']

    @action(
        methods=['GET', 'PATCH'],
        permission_classes=(permissions.IsAuthenticated,),
        detail=False,
        url_path='me'
    )
    def get_update_user(self, request):
        serializer = UserSerializer(request.user)
        if request.method == 'PATCH':
            serializer = NotAdminSerializer(
                request.user,
                data=request.data,
                partial=True)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.data)


class CategoryViewSet(CreateListDeleteViewSet):
    """Операции связананные с категориями"""
    queryset = Category.objects.all()
    serializer_class = CategorySerializer


class GenreViewSet(CreateListDeleteViewSet):
    """Операции связананные с жанрами"""
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer


class TitleViewSet(viewsets.ModelViewSet):
    """Операции связананные с названиями произведений"""
    queryset = Title.objects.all().annotate(
        rating=Avg('reviews__score')).order_by('name')
    permission_classes = (IsAdminOrReadOnly,)
    filter_backends = (DjangoFilterBackend,)
    filterset_class = TitleFilter

    def get_serializer_class(self):
        if self.request.method == 'PUT':
            raise MethodNotAllowed('PUT')
        if self.request.method in ('POST', 'PATCH',):
            return PostTitleSerializer
        return GetTitleSerializer


class ReviewViewSet(viewsets.ModelViewSet):
    permission_classes = (IsAuthorModeratorAdminOrReadOnly,)
    serializer_class = ReviewSerializer
    http_method_names = ['get', 'post', 'patch', 'delete']

    def get_title(self):
        title_id = self.kwargs.get('title_id')

        return get_object_or_404(Title, pk=title_id)

    def get_queryset(self):
        title = self.get_title()

        return title.reviews.all()

    def perform_create(self, serializer):
        serializer.save(author=self.request.user, title=self.get_title())


class CommentViewSet(viewsets.ModelViewSet):
    permission_classes = (IsAuthorModeratorAdminOrReadOnly,)
    serializer_class = CommentSerializer
    http_method_names = ['get', 'post', 'patch', 'delete']

    def get_queryset(self):
        review_id = self.kwargs.get('review_id')
        title_id = self.kwargs.get('title_id')
        review = get_object_or_404(Review, pk=review_id, title_id=title_id)

        return review.comments.all()

    def perform_create(self, serializer):
        review_id = self.kwargs.get('review_id')
        title_id = self.kwargs.get('title_id')
        review = get_object_or_404(Review, pk=review_id)
        serializer.save(author=self.request.user,
                        review=review,
                        title_id=title_id)
