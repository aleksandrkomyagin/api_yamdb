from django.urls import include, path
from rest_framework.routers import DefaultRouter

from api.views import (CategoryViewSet, CommentViewSet, GenreViewSet,
                       ReviewViewSet, TitleViewSet, UserViewSet,
                       get_confirmation_code, get_token_view)

v1_router = DefaultRouter()
v1_router.register('users', UserViewSet, basename='users')
v1_router.register(
    r'titles/(?P<title_id>\d+)/reviews',
    ReviewViewSet,
    basename='review')
v1_router.register(
    r'titles/(?P<title_id>\d+)/reviews/(?P<review_id>\d+)/comments',
    CommentViewSet,
    basename='comment')
v1_router.register('categories', CategoryViewSet, basename='categories')
v1_router.register('genres', GenreViewSet, basename='genres')
v1_router.register('titles', TitleViewSet, basename='titles')

app_name = 'api'

auth_urlpatterns = [
    path('signup/', get_confirmation_code, name='registration'),
    path('token/', get_token_view, name='token'),
]

urlpatterns = [
    path('v1/', include(v1_router.urls), name='router_urls'),
    path('v1/auth/', include(auth_urlpatterns), name='auth_urls'),
]
