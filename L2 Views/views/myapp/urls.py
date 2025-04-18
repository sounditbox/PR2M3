from django.urls import path, register_converter

from . import views, converters

app_name = "myapp"
register_converter(converters.FourDigitYearConverter, "year")
urlpatterns = [
    path("", views.index, name="home"),
    path('index/', views.redirect_to_index, name='index'),
    path("profile/<int:profile_id>/", views.profile, name="profile"),
]
