# Generated by Django 4.2 on 2023-06-07 16:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Brand', '0003_remove_profile_first_name_remove_profile_last_name_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='profile',
            name='full_name',
        ),
        migrations.AddField(
            model_name='profile',
            name='first_name',
            field=models.CharField(default=True, max_length=100),
        ),
        migrations.AddField(
            model_name='profile',
            name='last_name',
            field=models.CharField(default=1, max_length=100),
            preserve_default=False,
        ),
    ]
