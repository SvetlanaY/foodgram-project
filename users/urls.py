from django.urls import include, path

from . import views

urlpatterns = [
    path("auth/signup/", views.SignUp.as_view(), name="signup"),
    path("auth/", include("django.contrib.auth.urls")),
    path("<username>/", views.profile, name="profile"),
]
