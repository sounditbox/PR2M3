from django.db import models
from django.urls import reverse


class PublishedManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(is_published=True)


class Article(models.Model):
    author = models.ForeignKey('Author', on_delete=models.CASCADE, related_name='articles', null=True)
    title = models.CharField(max_length=200)
    tags = models.ManyToManyField('Tag', related_name='articles')
    content = models.TextField(blank=True)
    is_published = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    views = models.PositiveIntegerField(default=0)
    category = models.ForeignKey('Category', on_delete=models.PROTECT,
                                 null=True)

    published = PublishedManager()
    objects = models.Manager()

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('article_detail', kwargs={'pk': self.pk})

    def publish(self):
        if not self.is_published:
            self.is_published = True
            self.save(update_fields=['is_published'])


class Comment(models.Model):
    author = models.ForeignKey('Author', on_delete=models.PROTECT, related_name='comments', null=True)
    article = models.ForeignKey(Article,
                                on_delete=models.CASCADE,
                                related_name='comments')
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return self.content


class Category(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name


class Author(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name


class Tag(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name
# Categories
# Tags
# Authors
