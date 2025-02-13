# Generated by Django 5.1.3 on 2024-11-30 14:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("etl", "0003_norsemenshow"),
    ]

    operations = [
        migrations.CreateModel(
            name="VikingsShow",
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
                ("actor_url", models.URLField(max_length=500)),
                ("img_src", models.URLField(blank=True, max_length=500, null=True)),
                ("actor_name", models.CharField(max_length=255)),
                ("character_name", models.CharField(max_length=255, unique=True)),
                ("character_description", models.TextField(blank=True, null=True)),
            ],
            options={
                "verbose_name": "Vikings Show",
                "verbose_name_plural": "Vikings Show",
            },
        ),
    ]
