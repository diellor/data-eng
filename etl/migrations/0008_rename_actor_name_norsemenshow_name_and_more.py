# Generated by Django 5.1.4 on 2025-01-10 23:00

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("etl", "0007_scrapinglog"),
    ]

    operations = [
        migrations.RenameField(
            model_name="norsemenshow",
            old_name="actor_name",
            new_name="name",
        ),
        migrations.RenameField(
            model_name="vikingsnfl",
            old_name="player_name",
            new_name="name",
        ),
        migrations.RenameField(
            model_name="vikingsshow",
            old_name="actor_name",
            new_name="name",
        ),
    ]
