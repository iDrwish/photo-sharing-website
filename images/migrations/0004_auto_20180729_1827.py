# Generated by Django 2.0.6 on 2018-07-29 18:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('images', '0003_image_total_likes'),
    ]

    operations = [
        migrations.AlterField(
            model_name='image',
            name='total_likes',
            field=models.PositiveIntegerField(db_index=True, null=True),
        ),
    ]
