# Generated by Django 5.2 on 2025-04-18 16:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("myapp", "0001_initial"),
    ]

    operations = [
        migrations.AddField(
            model_name="profile",
            name="surname",
            field=models.CharField(max_length=50, null=True),
        ),
    ]
