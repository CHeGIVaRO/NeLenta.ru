# Generated by Django 2.2.5 on 2019-09-16 11:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('lenta', '0002_auto_20190913_1059'),
    ]

    operations = [
        migrations.AddField(
            model_name='news',
            name='newsimage',
            field=models.TextField(default='newsimage/', verbose_name='Путь к изображению новости'),
        ),
    ]