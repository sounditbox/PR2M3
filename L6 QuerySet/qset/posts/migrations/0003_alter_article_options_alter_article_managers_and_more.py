# Generated by Django 5.2 on 2025-05-06 17:44

import django.db.models.manager
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("posts", "0002_article_delete_post"),
    ]

    operations = [
        migrations.AlterModelOptions(
            name="article",
            options={"ordering": ["-created_at"]},
        ),
        migrations.AlterModelManagers(
            name="article",
            managers=[
                ("published", django.db.models.manager.Manager()),
            ],
        ),
        migrations.AddField(
            model_name="article",
            name="views",
            field=models.PositiveIntegerField(default=0),
        ),
    ]
