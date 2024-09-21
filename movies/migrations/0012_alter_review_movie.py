# Generated by Django 5.1.1 on 2024-09-21 18:16

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("movies", "0011_alter_review_movie"),
    ]

    operations = [
        migrations.AlterField(
            model_name="review",
            name="movie",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                to="movies.movie",
            ),
        ),
    ]
