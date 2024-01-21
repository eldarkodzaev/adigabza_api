# Generated by Django 4.2.7 on 2023-12-23 06:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('kab_rus_dictionary', '0010_alter_translation_same_words'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='translation',
            name='same_words',
        ),
        migrations.CreateModel(
            name='SameWords',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('translation', models.ManyToManyField(blank=True, to='kab_rus_dictionary.translation')),
            ],
        ),
    ]
