# Generated by Django 4.0.3 on 2022-07-10 18:27

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Blogs', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='blogpost',
            name='pub_date',
            field=models.DateTimeField(blank=True, default=datetime.datetime(2022, 7, 10, 18, 27, 26, 180466)),
        ),
    ]
