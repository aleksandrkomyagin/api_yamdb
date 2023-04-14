from django.urls import include, path
from rest_framework.routers import DefaultRouter
from api.views import get_confirmation_code, get_token_view, CategoriesViewSet, GenresViewSet, TitlesViewSet, CommentViewSet, ReviewViewSet, UserViewSet


v1_router = DefaultRouter()
v1_router.register(r'users', UserViewSet, basename='users')
v1_router.register(
    r'titles/(?P<title_id>\d+)/reviews',
    ReviewViewSet,
    basename='review')
v1_router.register(
    r'titles/(?P<title_id>\d+)/reviews/(?P<review_id>\d+)/comments',
    CommentViewSet,
    basename='comment')
v1_router.register(r'categories', CategoriesViewSet)
v1_router.register(r'genres', GenresViewSet)
v1_router.register(r'titles', TitlesViewSet)

app_name = 'api'

urlpatterns = [
    path('v1/', include(v1_router.urls), name='router_urls'),
    path('v1/auth/signup/', get_confirmation_code, name='registration'),
    path('v1/auth/token/', get_token_view, name='token'),
]
