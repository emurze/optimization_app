# Generated by Django 4.2.3 on 2023-07-28 16:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('services', '0002_alter_tariffplan_options'),
    ]

    operations = [
        migrations.AddField(
            model_name='tariffplan',
            name='title',
            field=models.CharField(default='Plan Type', max_length=128),
        ),
    ]
