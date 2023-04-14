import uuid

from django.contrib.auth import get_user_model
from django.core.mail import send_mail
from django.db import IntegrityError
from django.db.models import Avg
from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters, permissions, status, viewsets
from rest_framework.decorators import action, api_view, permission_classes
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from reviews.models import Category, EmailVerification, Genre, Review, Title

from .filters import TitleFilter
from .mixins import CreateListDeleteViewSet
from api.permissions import (IsAdminOrReadOnly, IsAdminUser,
                             IsAuthorModeratorAdminOrReadOnly)
from api.serializers import (AdminSerializer, CategorySerializer,
                             CommentSerializer, GenreSerializer,
                             GetTitleSerializer, NotAdminSerializer,
                             PostTitleSerializer, ReviewSerializer,
                             UserConfirmationCodeSerializer,
                             UserTokenSerializer)

User = get_user_model()


@api_view(['POST'])
@permission_classes([permissions.AllowAny])
def get_confirmation_code(request):
    username = request.data.get('username')
    email = request.data.get('email')
    serializers = UserConfirmationCodeSerializer(data=request.data)
    serializers.is_valid(raise_exception=True)
    username = serializers.validated_data.get('username')
    email = serializers.validated_data.get('email')
    try:
        user, sts = User.objects.get_or_create(username=username, email=email)
    except (User.DoesNotExist, IntegrityError) as er:
        return Response(
            {"Ошибка": f"{er}"},
            status=status.HTTP_400_BAD_REQUEST)
    if sts:
        code = uuid.uuid4()
        EmailVerification.objects.create(user=user, code=code)
    code = EmailVerification.objects.get(user=user).code
    send_mail(
        subject='Confirmation Code',
        message=f'Ваш код активации: {code}',
        recipient_list=[email, ],
        from_email='from@example.com',
    )
    return Response(serializers.data)


@api_view(['POST'])
@permission_classes([permissions.AllowAny])
def get_token_view(request):
    serializer = UserTokenSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    username = serializer.validated_data.get('username')
    try:
        user = User.objects.get(username=username)
    except User.DoesNotExist as er:
        return Response(
            {"Ошибка": f"{er}"},
            status=status.HTTP_404_NOT_FOUND)
    code = EmailVerification.objects.get(user=user).code
    if serializer.validated_data.get('confirmation_code') == str(code):
        token = RefreshToken.for_user(user).access_token
        return Response({'token': str(token)},
                        status=status.HTTP_201_CREATED)
    return Response(
        {'confirmation_code': 'Неверный код подтверждения!'},
        status=status.HTTP_400_BAD_REQUEST)


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = AdminSerializer
    permission_classes = (permissions.IsAuthenticated, IsAdminUser)
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
        serializer = AdminSerializer(request.user)
        if request.method == 'PATCH':
            if request.user.is_admin:
                serializer = AdminSerializer(
                    request.user,
                    data=request.data,
                    partial=True)
            else:
                serializer = NotAdminSerializer(
                    request.user,
                    data=request.data,
                    partial=True)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.data)

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        username = request.data['username']
        user = User.objects.get(username=username)
        code = uuid.uuid4()
        EmailVerification.objects.create(user=user, code=code)
        return Response(
            serializer.data,
            status=status.HTTP_201_CREATED,
            headers=headers
        )


class CategoryViewSet(CreateListDeleteViewSet):
    """Операции связананные с категориями"""
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = (IsAdminOrReadOnly,)
    filter_backends = [filters.SearchFilter]
    search_fields = ('name',)


class GenreViewSet(CreateListDeleteViewSet):
    """Операции связананные с жанрами"""
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer
    permission_classes = (IsAdminOrReadOnly,)
    filter_backends = [filters.SearchFilter]
    search_fields = ('name',)


class TitleViewSet(viewsets.ModelViewSet):
    """Операции связананные с названиями произведений"""
    queryset = Title.objects.all().annotate(
        Avg('reviews__score')).order_by('name')
    permission_classes = (IsAdminOrReadOnly,)
    filter_backends = (DjangoFilterBackend,)
    filterset_class = TitleFilter

    def get_serializer_class(self):
        if self.request.method in ('POST', 'PATCH',):
            return PostTitleSerializer
        return GetTitleSerializer


class ReviewViewSet(viewsets.ModelViewSet):
    permission_classes = (IsAuthorModeratorAdminOrReadOnly,)
    serializer_class = ReviewSerializer

    def check_title(self):
        title_id = self.kwargs.get('title_id')

        return get_object_or_404(Title, pk=title_id)

    def get_queryset(self):
        title = self.check_title()

        return title.reviews.all()

    def perform_create(self, serializer):
        serializer.save(author=self.request.user, title=self.check_title())


class CommentViewSet(viewsets.ModelViewSet):
    permission_classes = (IsAuthorModeratorAdminOrReadOnly,)
    serializer_class = CommentSerializer

    def get_queryset(self):
        review_id = self.kwargs.get('review_id')
        review = get_object_or_404(Review, pk=review_id)

        return review.comments.all()

    def perform_create(self, serializer):
        review_id = self.kwargs.get('review_id')
        review = get_object_or_404(Review, pk=review_id)
        serializer.save(author=self.request.user, review=review)
