# Generated by Django 4.2.17 on 2024-12-13 15:42

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("admin_management", "0001_initial"),
    ]

    operations = [
        migrations.AddField(
            model_name="admin",
            name="is_superuser",
            field=models.BooleanField(default=False),
        ),
    ]
