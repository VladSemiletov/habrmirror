# Generated by Django 4.0.6 on 2022-08-02 14:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('authapp', '0004_userhabs'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userhabs',
            name='description',
            field=models.TextField(blank=True, max_length=512, verbose_name='Описание'),
        ),
    ]
