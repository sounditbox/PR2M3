from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm


# class CreateUserForm(UserCreationForm):
#     class Meta:
#         model = get_user_model()
#         fields = ("username", "email", "password1", "password2")
#
#     def clean_password2(self):
#         password1 = self.cleaned_data.get("password1")
#         password2 = self.cleaned_data.get("password2")
#         if password1 and password2 and password1 != password2:
#             raise forms.ValidationError(
#                 self.error_messages["password_mismatch"],
#                 code="password_mismatch",
#             )
#         return password2
#
#     def clean_email(self):
#         email = self.cleaned_data.get("email")
#         if email and get_user_model().objects.filter(email=email).exists():
#             raise forms.ValidationError(
#                 self.error_messages["email_exists"],
#                 code="email_exists",
#             )
#         return email
