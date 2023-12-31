# Generated by Django 4.2 on 2023-09-29 16:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Brand', '0029_basket'),
    ]

    operations = [
        migrations.CreateModel(
            name='Order',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('user_name', models.CharField(max_length=255)),
                ('last_name', models.CharField(max_length=255)),
                ('middle_name', models.CharField(max_length=255)),
                ('phone_number', models.CharField(max_length=20)),
                ('country', models.CharField(max_length=100)),
                ('city', models.CharField(max_length=100)),
                ('payment_method', models.CharField(max_length=100)),
            ],
        ),
    ]
