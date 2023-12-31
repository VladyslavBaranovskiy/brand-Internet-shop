# Generated by Django 4.2 on 2023-06-15 10:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Brand', '0016_alter_productcatalog_size'),
    ]

    operations = [
        migrations.CreateModel(
            name='ProductImage',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', models.ImageField(upload_to='product_image/')),
            ],
        ),
        migrations.AlterField(
            model_name='productcatalog',
            name='size',
            field=models.CharField(max_length=255),
        ),
        migrations.AddField(
            model_name='productcatalog',
            name='images',
            field=models.ManyToManyField(related_name='products', to='Brand.productimage'),
        ),
    ]
