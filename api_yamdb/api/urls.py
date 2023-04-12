from django.urls import path

from api.views import get_confirmation_code, get_token_view


app_name = 'api'

urlpatterns = [
    path('v1/auth/signup/', get_confirmation_code, name='registration'),
    path('v1/auth/token/', get_token_view, name='token'),
]
