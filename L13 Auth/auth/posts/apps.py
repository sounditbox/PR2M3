from django.apps import AppConfig


class PostsConfig(AppConfig):
    verbose_name = "Blog"
    default_auto_field = "django.db.models.BigAutoField"
    name = "posts"
