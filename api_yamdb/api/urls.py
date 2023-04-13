from django.urls import include, path
from rest_framework.routers import DefaultRouter

from api.views import get_confirmation_code, get_token_view

from .views import CategoriesViewSet, GenresViewSet, TitlesViewSet

app_name = 'api'

router = DefaultRouter()
router.register(r'categories', CategoriesViewSet)
router.register(r'genres', GenresViewSet)
router.register(r'titles', TitlesViewSet)

urlpatterns = [
    path('v1/', include(router.urls)),
    path('v1/auth/signup/', get_confirmation_code, name='registration'),
    path('v1/auth/token/', get_token_view, name='token')
]
