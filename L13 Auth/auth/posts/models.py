from django.db import models
from django.urls import reverse


class TimeStampedModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class Article(TimeStampedModel):
    STATUS_CHOICES = (
        ('draft', 'Draft'),
        ('published', 'Published'),
        ('archived', 'Archived'),
        ('deleted', 'Deleted'),
    )

    author = models.ForeignKey('Author', on_delete=models.CASCADE,
                               related_name='articles', null=True)
    title = models.CharField(max_length=200)
    tags = models.ManyToManyField('Tag', related_name='articles')
    content = models.TextField(blank=True)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES,
                              default=STATUS_CHOICES[0][0])

    image = models.ImageField(upload_to='images/', null=True)

    views = models.PositiveIntegerField(default=0)
    category = models.ForeignKey('Category', on_delete=models.PROTECT,
                                 null=True)

    objects = models.Manager()

    class Meta:
        ordering = ["-created_at"]
        indexes = [
            models.Index(fields=['-created_at']),

        ]
        verbose_name = "Post"
        verbose_name_plural = "Posts"

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('article_detail', kwargs={'pk': self.pk})

    def publish(self):
        if not self.status:
            self.status = True
            self.save(update_fields=['is_published'])


class Comment(TimeStampedModel):
    author = models.ForeignKey('Author', on_delete=models.PROTECT,
                               related_name='comments', null=True)
    article = models.ForeignKey(Article,
                                on_delete=models.PROTECT,
                                related_name='comments')
    content = models.TextField()

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return self.content


class Category(models.Model):
    name = models.CharField(max_length=50)

    class Meta:
        verbose_name_plural = "Categories"

    def __str__(self):
        return self.name


class Author(models.Model):
    name = models.CharField(max_length=50)
    user = models.OneToOneField('auth.User', on_delete=models.PROTECT, null=True)

    def __str__(self):
        return self.name


class Tag(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name
