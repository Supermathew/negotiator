# Generated by Django 5.0.6 on 2024-08-08 08:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("chatbot", "0001_initial"),
    ]

    operations = [
        migrations.AlterField(
            model_name="usersession",
            name="state",
            field=models.JSONField(default=dict),
        ),
    ]
