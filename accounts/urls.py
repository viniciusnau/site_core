from django.urls import path
from django.views.decorators.csrf import csrf_exempt

from .views import GoogleLoginApi, GoogleLoginRedirectApi, MeView

urlpatterns = [
    path("me/", MeView.as_view(), name="me"),
    path(
        "google-redirect/",
        csrf_exempt(GoogleLoginRedirectApi.as_view()),
        name="google-redirect",
    ),
    path("google-login/", csrf_exempt(GoogleLoginApi.as_view()), name="google-login"),
]
