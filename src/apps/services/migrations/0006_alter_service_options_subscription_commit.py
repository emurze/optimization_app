# Generated by Django 4.2.3 on 2023-07-31 10:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('services', '0005_subscription_price'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='service',
            options={'ordering': ('title',)},
        ),
        migrations.AddField(
            model_name='subscription',
            name='commit',
            field=models.CharField(default=''),
        ),
    ]
