# Generated by Django 3.2.9 on 2021-12-13 12:00

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('mainapp', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=128, unique=True, verbose_name='имя')),
                ('description', models.TextField(blank=True, verbose_name='описание')),
                ('short_description', models.CharField(blank=True, max_length=64, verbose_name='короткое описание')),
                ('price', models.DecimalField(decimal_places=2, default=0, max_digits=8, verbose_name='цена со скидкой')),
                ('quantity', models.IntegerField(default=0, verbose_name='кол-во на складе')),
                ('image', models.ImageField(blank=True, upload_to='products_images')),
                ('category', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='mainapp.productcategory')),
            ],
        ),
    ]
