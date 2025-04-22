from django.urls import path

from .views import index, show_user_profile, profiles

urlpatterns = [
    path("", index, name="index"),
    path('profile/<int:user_id>/', show_user_profile, name='profile'),
    path('profiles', profiles, name='profiles'),
]
