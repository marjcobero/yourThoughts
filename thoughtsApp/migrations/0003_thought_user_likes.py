# Generated by Django 2.2 on 2021-03-26 05:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('thoughtsApp', '0002_auto_20210326_0528'),
    ]

    operations = [
        migrations.AddField(
            model_name='thought',
            name='user_likes',
            field=models.ManyToManyField(related_name='liked_posts', to='thoughtsApp.User'),
        ),
    ]
