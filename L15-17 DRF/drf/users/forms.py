from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm


class CreateUserForm(UserCreationForm):
    class Meta:
        model = get_user_model()
        fields = ("avatar", "username", "email", "password1", "password2")

        widgets = {
            "username": forms.TextInput(attrs={"class": "form-control"}),
            "email": forms.EmailInput(attrs={"class": "form-control"}),
            "password1": forms.PasswordInput(attrs={"class": "form-control"}),
            "password2": forms.PasswordInput(attrs={"class": "form-control"}),
            "avatar": forms.FileInput(attrs={"class": "form-control"}),
        }

        labels = {
            "avatar": "Аватар",
            "username": "Юзернейм",
            "email": "Почта",
            "password1": "Пароль",
            "password2": "Подтверждение пароля",
        }


class ProfileForm(forms.ModelForm):
    class Meta:
        model = get_user_model()
        fields = ("avatar", "username", "email")
        readonly_fields = ("username", "email")

        widgets = {
            "username": forms.TextInput(
                attrs={"class": "form-control", "readonly": "readonly"}),
            "email": forms.EmailInput(
                attrs={"class": "form-control", "readonly": "readonly"}),
            "avatar": forms.FileInput(attrs={"class": "form-control"}),
        }

        labels = {
            "avatar": "Аватар",
            "username": "Юзернейм",
            "email": "Почта",
        }
