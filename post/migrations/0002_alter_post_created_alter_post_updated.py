# Generated by Django 5.0 on 2023-12-07 11:44

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("post", "0001_initial"),
    ]

    operations = [
        migrations.AlterField(
            model_name="post",
            name="created",
            field=models.DateTimeField(auto_now=True),
        ),
        migrations.AlterField(
            model_name="post",
            name="updated",
            field=models.DateTimeField(auto_now=True),
        ),
    ]
