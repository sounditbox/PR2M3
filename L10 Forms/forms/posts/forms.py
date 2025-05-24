from django.core.exceptions import ValidationError
from django.forms import fields, ModelForm, TextInput, Textarea, Select, \
    SelectMultiple, Form

from .models import Article, Comment  # Импорт модели


class ContactForm(Form):
    subject = fields.CharField(max_length=100, min_length=3, label="Тема",

                               widget=fields.TextInput(attrs={
                                   'class': 'form-control form-control-lg',
                                   'placeholder': 'Введите тему сообщения'}))
    name = fields.CharField(
        label="Имя",
        widget=fields.TextInput(attrs={
            'class': 'form-control form-control-lg',
            'placeholder': 'Введите ваше полное имя'
        })
    )
    message = fields.CharField(
        label="Сообщение",
        widget=fields.Textarea(attrs={
            'class': 'form-control',
            'rows': 5,  # Устанавливаем количество строк
            'cols': 40,  # Устанавливаем количество колонок
            'placeholder': 'Введите ваше сообщение'
        })
    )
    agree = fields.BooleanField(
        label="Согласен с условиями",
        widget=fields.CheckboxInput(
            attrs={'class': 'form-control form-check-input'})
    )

    def clean_message(self):
        message = self.cleaned_data["message"]
        if "spam" in message:
            raise ValidationError("Spam is not allowed")
        return message

    def clean_sender(self):
        sender = self.cleaned_data["sender"]
        if "spam" in sender:
            raise ValidationError("Spam is not allowed")
        return sender


class ArticleCreateForm(ModelForm):
    extra_field = fields.CharField(
        required=False,
        widget=fields.Textarea(
            attrs={'class': 'form-control', 'placeholder': 'Доп.инфо'})

    )

    class Meta:
        model = Article  # Указываем модель
        fields = ["title", "content", "status", "category", 'tags']
        widgets = {
            'title': TextInput(attrs={'class': 'form-control'}),
            'content': Textarea(attrs={'class': 'form-control'}),
            'status': Select(attrs={'class': 'form-control'}),
            'category': Select(attrs={'class': 'form-control'}),
            'tags': SelectMultiple(attrs={'class': 'form-control'}),
        }
        labels = {
            'title': 'Заголовок',
            'content': 'Текст',
            'status': 'Статус',
            'category': 'Категория',
            'tags': 'Теги',
        }


class ArticleEditForm(ModelForm):
    class Meta:
        model = Article  # Указываем модель
        fields = ["title", "content", "status", ]
        widgets = {
            'title': TextInput(attrs={'class': 'form-control'}),
            'content': Textarea(attrs={'class': 'form-control'}),
            'status': Select(attrs={'class': 'form-control'}),
        }
        labels = {
            'title': 'Заголовок',
            'content': 'Текст',
            'status': 'Статус',
        }


class CommentForm(ModelForm):
    class Meta:
        model = Comment
        fields = ['content']
        widgets = {
            'content': Textarea(attrs={'class': 'form-control',
                                       'placeholder': "Введите комментарий"}),
        }
        labels = {
            'content': 'Комментарий'
        }
