from django.contrib import messages
from django.contrib.auth import login, get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpRequest, HttpResponse
from django.shortcuts import redirect, render
from django.views.generic import DetailView, UpdateView

from .forms import CreateUserForm, ProfileForm


def register_view(request: HttpRequest) -> HttpResponse:
    if request.method == 'POST':
        form = CreateUserForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, 'Пользователь успешно создан')
            return redirect('users:profile')
        else:
            print(form.errors)
            messages.error(request, f'Заполните форму правильно!')
            return redirect('users:register')
    else:
        form = CreateUserForm()
    return render(request, 'users/register.html', context={'form': form})


class ProfileView(UpdateView, LoginRequiredMixin):
    model = get_user_model()
    form_class = ProfileForm
    template_name = 'users/profile.html'

    def get_object(self, queryset=None):
        return self.request.user

