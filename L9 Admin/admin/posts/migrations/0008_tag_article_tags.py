# Generated by Django 5.2.1 on 2025-05-13 17:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("posts", "0007_author_article_author_comment_author"),
    ]

    operations = [
        migrations.CreateModel(
            name="Tag",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("name", models.CharField(max_length=50)),
            ],
        ),
        migrations.AddField(
            model_name="article",
            name="tags",
            field=models.ManyToManyField(related_name="articles", to="posts.tag"),
        ),
    ]
