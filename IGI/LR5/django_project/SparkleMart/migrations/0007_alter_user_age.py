# Generated by Django 4.1.7 on 2024-04-29 15:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('SparkleMart', '0006_user_age'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='age',
            field=models.PositiveSmallIntegerField(default=100),
        ),
    ]