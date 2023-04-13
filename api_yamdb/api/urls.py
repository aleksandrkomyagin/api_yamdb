from django.urls import include, path

from rest_framework.routers import DefaultRouter

from api.views import get_confirmation_code, get_token_view, UserViewSet

v1_router = DefaultRouter()
v1_router.register(r'users', UserViewSet, basename='users')

app_name = 'api'

urlpatterns = [
    path('v1/auth/signup/', get_confirmation_code, name='registration'),
    path('v1/auth/token/', get_token_view, name='token'),
    path('v1/', include(v1_router.urls), name='router_urls'),
]
