# Generated by Django 2.2 on 2019-11-05 03:06

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('webapp', '0006_team'),
    ]

    operations = [
        migrations.AddField(
            model_name='issue',
            name='assigned_to',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.PROTECT, related_name='assigned_issues', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='issue',
            name='created_by',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.PROTECT, related_name='created_issues', to=settings.AUTH_USER_MODEL),
        ),
    ]
