from django.urls import include, path
from rest_framework.routers import DefaultRouter

from api.views import get_confirmation_code, get_token_view, CategoriesViewSet, GenresViewSet, TitlesViewSet, CommentViewSet, ReviewViewSet


router = DefaultRouter()

app_name = 'api'

router.register(
    r'titles/(?P<title_id>\d+)/reviews',
    ReviewViewSet,
    basename='review')
router.register(
    r'titles/(?P<title_id>\d+)/reviews/(?P<review_id>\d+)/comments',
    CommentViewSet,
    basename='comment')

router.register(r'categories', CategoriesViewSet)
router.register(r'genres', GenresViewSet)
router.register(r'titles', TitlesViewSet)

urlpatterns = [
    path('v1/', include(router.urls)),
    path('v1/auth/signup/', get_confirmation_code, name='registration'),
    path('v1/auth/token/', get_token_view, name='token'),
]
