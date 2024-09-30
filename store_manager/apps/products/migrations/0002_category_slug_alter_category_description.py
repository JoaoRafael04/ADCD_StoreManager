# Generated by Django 5.1.1 on 2024-09-30 16:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("products", "0001_initial"),
    ]

    operations = [
        migrations.AddField(
            model_name="category",
            name="slug",
            field=models.SlugField(blank=True, unique=True),
        ),
        migrations.AlterField(
            model_name="category",
            name="description",
            field=models.TextField(blank=True),
        ),
    ]