# Generated by Django 4.2 on 2023-06-16 11:42

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('Brand', '0018_remove_productcatalog_images_delete_productimage'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='productcatalog',
            name='image',
        ),
        migrations.CreateModel(
            name='Image',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', models.ImageField(upload_to='product_image/')),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='image', to='Brand.productcatalog')),
            ],
        ),
        migrations.AddField(
            model_name='productcatalog',
            name='images',
            field=models.ManyToManyField(to='Brand.image'),
        ),
    ]
