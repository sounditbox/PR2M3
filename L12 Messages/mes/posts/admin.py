from django.contrib import admin, messages
from django.utils.safestring import mark_safe

from .models import Article, Tag, Category, Author, Comment

admin.site.site_title = "Blog Admin Site"
admin.site.site_header = "Blog Admin"
admin.site.index_title = "Welcome to Blog Admin"


# Действие для публикации

def make_published(article, request, queryset):
    updated = queryset.update(status=Article.STATUS_CHOICES[1][0],
                              author=request.user)
    article.message_user(request, f"{updated} постов было опубликовано.",
                         messages.SUCCESS)
    make_published.short_description = "Опубликовать выбранные посты"


# Действие для снятия с публикации
def make_draft(modeladmin, request, queryset):
    updated = queryset.update(status=Article.STATUS_CHOICES[0][0])
    modeladmin.message_user(request, f"{updated} постов снято с публикации.",
                            messages.SUCCESS)
    make_draft.short_description = "Сделать черновиком"


def make_archived(modeladmin, request, queryset):
    updated = queryset.update(status=Article.STATUS_CHOICES[2][0])
    modeladmin.message_user(request, f"{updated} постов снято с публикации.",
                            messages.SUCCESS)
    make_archived.short_description = "Заархивировать"


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('id', "article", "author", "content", "created_at")
    list_editable = ('article', 'author', "content")


class CommentInline(admin.TabularInline):
    model = Comment
    extra = 1
    max_num = 5
    min_num = 1
    fields = ('author', 'content', 'created_at')
    readonly_fields = ('created_at',)
    classes = ('collapse',)


@admin.register(Article)
class ArticleAdmin(admin.ModelAdmin):
    list_display = ("title", "status",
                    "author", "category", "created_at", "unmodified_since",
                    'image_admin')
    list_display_links = ("title",)
    list_editable = ("status", 'category', 'author')
    list_filter = ("status", 'category', 'author')
    search_fields = ("title", "content", "tags__name")
    ordering = ["created_at"]
    actions = [make_published, make_draft, make_archived]

    readonly_fields = ("created_at", "updated_at", "views")
    inlines = (CommentInline,)
    fieldsets = (
        ('Основная информация', {
            'fields': ('title', 'author', 'status', 'views', 'category')
        }),
        ('Содержимое поста', {
            'fields': ('content', 'image', 'tags'),
            'classes': ('collapse',),
            'description': 'Основной текст и теги для поста.'
        }),
        ('Даты (Авто)', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )

    @admin.display(description="Last modified", ordering="updated_at")
    def unmodified_since(self, article: Article):
        if article.created_at == article.updated_at:
            return "Unmodified"
        return str(article.updated_at - article.created_at).split(".")[0]

    @admin.display(description="Image")
    def image_admin(self, article: Article):
        if article.image:
            return mark_safe(
                f'<img src="{article.image.url}" width="100"/>')
        return "None"


admin.site.register(Tag)
admin.site.register(Category)
admin.site.register(Author)

# admin.site.register(Comment)
