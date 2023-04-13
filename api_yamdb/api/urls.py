from django.urls import include, path
from rest_framework.routers import DefaultRouter

from api.views import get_confirmation_code, get_token_view

from . import views

router = DefaultRouter()

app_name = 'api'

router.register(
    r'titles/(?P<title_id>\d+)/reviews',
    views.ReviewViewSet,
    basename='review')
router.register(
    r'titles/(?P<title_id>\d+)/reviews/(?P<review_id>\d+)/comments',
    views.CommentViewSet,
    basename='comment')

urlpatterns = [
    path('v1/', include(router.urls)),
    path('v1/registration/', get_confirmation_code, name='registration'),
    path('v1/token/', get_token_view, name='token'),
]
