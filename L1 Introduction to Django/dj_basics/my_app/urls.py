from django.urls import path
from .views import index, profile

urlpatterns = [
    path("", index),
    path("profile/<int:profile_id>/", profile, name="profile"),
]
