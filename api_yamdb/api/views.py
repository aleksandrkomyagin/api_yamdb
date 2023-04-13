import uuid

from django.contrib.auth import get_user_model
from django.core.mail import send_mail
from django.db import IntegrityError
from rest_framework import filters, permissions, status, viewsets
from rest_framework.decorators import action, api_view, permission_classes
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from reviews.models import EmailVerification

from api.permissions import IsAdminUser
from api.serializers import (AdminSerializer, NotAdminSerializer,
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
