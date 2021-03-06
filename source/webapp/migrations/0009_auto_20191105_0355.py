# Generated by Django 2.2 on 2019-11-05 03:55

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('webapp', '0008_auto_20191105_0352'),
    ]

    operations = [
        migrations.AlterField(
            model_name='issue',
            name='assigned_to',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.PROTECT, related_name='assigned_issues', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='issue',
            name='created_by',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.PROTECT, related_name='created_issues', to=settings.AUTH_USER_MODEL),
        ),
    ]
