# Generated by Django 5.1.7 on 2025-05-30 12:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('teams', '0010_alter_team_created_by'),
    ]

    operations = [
        migrations.AlterField(
            model_name='team',
            name='email',
            field=models.EmailField(blank=True, max_length=254),
        ),
    ]
