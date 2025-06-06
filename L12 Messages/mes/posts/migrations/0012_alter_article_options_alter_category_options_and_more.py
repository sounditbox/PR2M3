# Generated by Django 5.2.1 on 2025-05-27 16:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("posts", "0011_article_updated_at"),
    ]

    operations = [
        migrations.AlterModelOptions(
            name="article",
            options={
                "ordering": ["-created_at"],
                "verbose_name": "Post",
                "verbose_name_plural": "Posts",
            },
        ),
        migrations.AlterModelOptions(
            name="category",
            options={"verbose_name_plural": "Categories"},
        ),
        migrations.AddField(
            model_name="article",
            name="image",
            field=models.ImageField(blank=True, null=True, upload_to="images/"),
        ),
    ]
