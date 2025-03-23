# Generated by Django 5.1.6 on 2025-03-09 09:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('web', '0002_comment_rate'),
    ]

    operations = [
        migrations.AlterField(
            model_name='comment',
            name='rate',
            field=models.IntegerField(choices=[(1, 1), (2, 2), (3, 3), (4, 4), (5, 5)], default=0),
        ),
    ]
