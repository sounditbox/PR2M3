from django.contrib import messages
from django.contrib.auth import login
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.views import LoginView
from django.http import HttpRequest, HttpResponse
from django.shortcuts import redirect, render
from django.urls import reverse_lazy
from django.views.generic import CreateView



# def login_view(request: HttpRequest) -> HttpResponse:
#     if request.method == 'POST':
#         form = LoginForm(request.POST)
#         if form.is_valid():
#             cd = form.cleaned_data
#             user = authenticate(request, username=cd['username'],
#                                 password=cd['password'])
#             if user is not None and user.is_active:
#                 login(request, user)
#             return redirect('article_list')
#
#     else:
#         form = LoginForm()
#     return render(request, 'users/login.html', context={'form': form})
#
#
# @login_required
# def logout_view(request: HttpRequest) -> HttpResponse:
#     logout(request)
#     return redirect('article_list')

class CustomLoginView(LoginView):
    template_name = 'users/login.html'


# class RegisterView(CreateView):
#     template_name = 'users/register.html'
#     form_class = CreateUserForm
#     success_url = reverse_lazy('article_list')
#
#     def form_valid(self, form):
#         form.save()
#         return super().form_valid(form)


def register_view(request: HttpRequest) -> HttpResponse:
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, 'Пользователь успешно создан')
            return redirect('article_list')
        else:
            messages.error(request, f'Заполните форму правильно! {form.errors}')
    else:
        form = UserCreationForm()
    return render(request, 'users/register.html', context={'form': form})

