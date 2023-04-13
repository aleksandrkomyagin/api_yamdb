from django.urls import include, path
from rest_framework.routers import DefaultRouter

from api.views import get_confirmation_code, get_token_view

from .views import CategoriesViewSet, GenresViewSet, TitlesViewSet

app_name = 'api'

router = DefaultRouter()
router.register(r'v1/categories', CategoriesViewSet)
router.register(r'v1/genres', GenresViewSet)
router.register(r'v1/titles', TitlesViewSet)

urlpatterns = [
    path('v1/registration/', get_confirmation_code, name='registration'),
    path('v1/token/', get_token_view, name='token'),
    path('', include(router.urls)),
]
