# Generated by Django 2.1 on 2018-09-02 15:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('polls', '0004_remove_media_tipo'),
    ]

    operations = [
        migrations.AddField(
            model_name='media',
            name='tipo',
            field=models.CharField(blank=True, max_length=30),
        ),
    ]
