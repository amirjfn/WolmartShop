# Generated by Django 4.2.1 on 2023-06-13 19:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='backgroundcolor',
            options={'verbose_name': 'رنگ بک گراند', 'verbose_name_plural': 'رنگ بک گراند ها'},
        ),
        migrations.AddField(
            model_name='backgroundcolor',
            name='color_name',
            field=models.CharField(max_length=30, null=True, verbose_name='رنگ محصول'),
        ),
    ]