# Generated by Django 4.2.7 on 2023-12-10 11:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('kab_rus_dictionary', '0002_alter_translation_categories'),
    ]

    operations = [
        migrations.AlterField(
            model_name='translation',
            name='categories',
            field=models.ManyToManyField(blank=True, default=None, null=True, to='kab_rus_dictionary.category'),
        ),
    ]
