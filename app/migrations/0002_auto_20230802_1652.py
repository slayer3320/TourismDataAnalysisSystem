# Generated by Django 2.2.14 on 2023-08-02 08:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='textarea',
            field=models.CharField(default='这个人很懒，什么有没留下。', max_length=255, verbose_name='个人简介'),
        ),
    ]
