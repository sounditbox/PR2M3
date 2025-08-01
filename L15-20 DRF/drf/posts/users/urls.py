from django.contrib.auth.views import LogoutView, PasswordResetView, \
    PasswordResetDoneView, PasswordResetConfirmView, PasswordResetCompleteView, \
    LoginView
from django.urls import path, reverse_lazy
from .views import register_view, ProfileView

app_name = 'users'


urlpatterns = [
    path('profile/', ProfileView.as_view(), name='profile'),

    path('login/', LoginView.as_view(
        template_name='users/login.html',
        success_url=reverse_lazy('users:profile')),
         name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('register/', register_view, name='register'),

    path('password_reset/', PasswordResetView.as_view(
        template_name='users/password_reset.html',
        success_url=reverse_lazy('users:password_reset_done'),
        email_template_name='users/password_reset_email.html'
    ), name='password_reset'),

    path(
        'password_reset/done/', PasswordResetDoneView.as_view(
            template_name='users/password_reset_done.html'
        ), name='password_reset_done'),

    path(
        'password_reset/confirm/<uidb64>/<token>/',
        PasswordResetConfirmView.as_view(
            template_name='users/password_reset_confirm.html',
            success_url=reverse_lazy('users:password_reset_complete')
        ), name='password_reset_confirm'
    ),

    path(
        'password_reset/complete/',
        PasswordResetCompleteView.as_view(
            template_name='users/password_reset_complete.html'
        ), name='password_reset_complete'
    ),
]

