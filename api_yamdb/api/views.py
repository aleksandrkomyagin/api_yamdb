import uuid

from django.shortcuts import get_object_or_404
from django.contrib.auth import get_user_model
from django.core.mail import send_mail
from rest_framework import viewsets

from rest_framework.decorators import api_view, permission_classes
from rest_framework import permissions, viewsets
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework import status
from rest_framework.pagination import LimitOffsetPagination

from api.serializers import (CreateUserToken,
                             CreateUserConfirmationCode,
                             CommentSerializer,
                             ReviewSerializer)
from reviews.models import EmailVerification, Review, Title
from .permissions import IsAuthorOrReadOnlyPermission


User = get_user_model()


@api_view(['POST'])
@permission_classes([permissions.AllowAny])
def get_confirmation_code(request):
    serializers = CreateUserConfirmationCode(data=request.data)
    serializers.is_valid(raise_exception=True)
    username = serializers.validated_data.get('username')
    email = serializers.validated_data.get('email')
    user, status = User.objects.get_or_create(username=username, email=email)
    if status:
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
    serializer = CreateUserToken(data=request.data)
    serializer.is_valid(raise_exception=True)
    username = serializer.validated_data.get('username')
    user = User.objects.get(username=username)
    code = EmailVerification.objects.get(user=user).code
    if serializer.validated_data.get('confirmation_code') == str(code):
        token = RefreshToken.for_user(user).access_token
        return Response({'token': str(token)},
                        status=status.HTTP_201_CREATED)
    return Response(
        {'confirmation_code': 'Неверный код подтверждения!'},
        status=status.HTTP_400_BAD_REQUEST)


class ReviewViewSet(viewsets.ModelViewSet):
    permission_classes = (IsAuthorOrReadOnlyPermission,)
    pagination_class = LimitOffsetPagination
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
    permission_classes = (IsAuthorOrReadOnlyPermission,)
    pagination_class = LimitOffsetPagination
    serializer_class = CommentSerializer

    def get_queryset(self):
        review_id = self.kwargs.get('review_id')
        review = get_object_or_404(Review, pk=review_id)

        return review.comments.all()

    def perform_create(self, serializer):
        review_id = self.kwargs.get('review_id')
        review = get_object_or_404(Review, pk=review_id)
        serializer.save(author=self.request.user, review=review)
