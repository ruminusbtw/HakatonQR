# Generated by Django 5.1.3 on 2024-11-20 16:17

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("attendance", "0001_initial"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="attendance",
            name="scanned_at",
        ),
    ]
