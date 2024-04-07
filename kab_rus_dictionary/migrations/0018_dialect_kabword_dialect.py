# Generated by Django 4.2.7 on 2024-03-31 07:54

from django.db import migrations, models
import django.db.models.deletion
import kab_rus_dictionary.models


class Migration(migrations.Migration):

    dependencies = [
        ('kab_rus_dictionary', '0017_remove_kabword_synonym_kabword_synonyms'),
    ]

    operations = [
        migrations.CreateModel(
            name='Dialect',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('dialect_rus', models.CharField(max_length=20)),
                ('dialect_kab', models.CharField(max_length=30)),
            ],
            options={
                'ordering': ('dialect_rus',),
                'unique_together': {('dialect_rus', 'dialect_kab')},
            },
        ),
        migrations.AddField(
            model_name='kabword',
            name='dialect',
            field=models.ForeignKey(default=kab_rus_dictionary.models.Dialect.get_default_dialect, on_delete=django.db.models.deletion.SET_DEFAULT, to='kab_rus_dictionary.dialect'),
        ),
    ]
