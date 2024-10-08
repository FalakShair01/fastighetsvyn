# Generated by Django 4.2.6 on 2024-08-25 13:02

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    initial = True

    dependencies = [
        ("property", "0001_initial"),
        ("users", "0001_initial"),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ("feedback", "0001_initial"),
    ]

    operations = [
        migrations.AddField(
            model_name="userfeedback",
            name="property",
            field=models.ForeignKey(
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                to="property.property",
            ),
        ),
        migrations.AddField(
            model_name="userfeedback",
            name="tenant",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE, to="users.tenant"
            ),
        ),
        migrations.AddField(
            model_name="userfeedback",
            name="user",
            field=models.ForeignKey(
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                related_name="feedbacks",
                to=settings.AUTH_USER_MODEL,
            ),
        ),
        migrations.AddField(
            model_name="adminfeedback",
            name="user",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name="admin_feedback",
                to=settings.AUTH_USER_MODEL,
            ),
        ),
    ]
