# Generated by Django 5.0.3 on 2024-03-18 21:18

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='banner',
            options={'ordering': ['-id'], 'verbose_name': 'Баннер', 'verbose_name_plural': 'Баннеры'},
        ),
        migrations.AlterModelOptions(
            name='category',
            options={'ordering': ['order'], 'verbose_name': 'Категория', 'verbose_name_plural': 'Категории'},
        ),
        migrations.AlterModelOptions(
            name='info',
            options={'ordering': ['-id'], 'verbose_name': 'Инфо', 'verbose_name_plural': 'Инфо'},
        ),
        migrations.AlterModelOptions(
            name='settings',
            options={'ordering': ['-id'], 'verbose_name': 'Настройка', 'verbose_name_plural': 'Настройки'},
        ),
    ]
