# Generated by Django 4.2.7 on 2024-06-22 13:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('kab_rus_dictionary', '0018_dialect_kabword_dialect'),
    ]

    operations = [
        migrations.AddField(
            model_name='language',
            name='slug',
            field=models.SlugField(default=1, max_length=40),
            preserve_default=False,
        ),
    ]
