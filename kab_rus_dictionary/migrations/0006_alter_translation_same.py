# Generated by Django 4.2.7 on 2023-12-22 16:35

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('kab_rus_dictionary', '0005_translation_same'),
    ]

    operations = [
        migrations.AlterField(
            model_name='translation',
            name='same',
            field=models.ForeignKey(blank=True, default=None, null=True, on_delete=django.db.models.deletion.SET_DEFAULT, related_name='sames', to='kab_rus_dictionary.translation'),
        ),
    ]
