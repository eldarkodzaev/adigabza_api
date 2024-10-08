# Generated by Django 4.2.7 on 2023-12-04 17:26

from django.db import migrations, models
import django.db.models.deletion
import mptt.fields


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('kab_alphabet', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(db_index=True, max_length=100)),
                ('slug', models.SlugField(max_length=100)),
                ('lft', models.PositiveIntegerField(editable=False)),
                ('rght', models.PositiveIntegerField(editable=False)),
                ('tree_id', models.PositiveIntegerField(db_index=True, editable=False)),
                ('level', models.PositiveIntegerField(editable=False)),
                ('parent', mptt.fields.TreeForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='children', to='kab_rus_dictionary.category')),
            ],
            options={
                'verbose_name': 'category',
                'verbose_name_plural': 'categories',
            },
        ),
        migrations.CreateModel(
            name='KabWord',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('word', models.CharField(max_length=100, unique=True)),
                ('slug', models.SlugField(max_length=100, unique=True)),
            ],
            options={
                'ordering': ('letter__id', 'word'),
            },
        ),
        migrations.CreateModel(
            name='Language',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=30)),
            ],
            options={
                'ordering': ('name',),
            },
        ),
        migrations.CreateModel(
            name='PartOfSpeech',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=30)),
            ],
            options={
                'verbose_name': 'part of speech',
                'verbose_name_plural': 'parts of speech',
                'ordering': ('name',),
            },
        ),
        migrations.CreateModel(
            name='Source',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=300)),
                ('author', models.CharField(max_length=200)),
                ('year', models.PositiveIntegerField(blank=True, null=True)),
                ('url', models.URLField(blank=True, null=True)),
            ],
            options={
                'ordering': ('name',),
            },
        ),
        migrations.CreateModel(
            name='Translation',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('translation', models.TextField()),
                ('description', models.TextField(blank=True, null=True)),
                ('categories', models.ManyToManyField(to='kab_rus_dictionary.category')),
                ('part_of_speech', models.ForeignKey(blank=True, default=None, null=True, on_delete=django.db.models.deletion.SET_DEFAULT, related_name='words', to='kab_rus_dictionary.partofspeech')),
                ('source', models.ForeignKey(blank=True, default=None, null=True, on_delete=django.db.models.deletion.SET_DEFAULT, related_name='words', to='kab_rus_dictionary.source')),
                ('word', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='translations', to='kab_rus_dictionary.kabword')),
            ],
            options={
                'ordering': ('word__letter__id', 'word'),
            },
        ),
        migrations.AddField(
            model_name='kabword',
            name='borrowed_from',
            field=models.ForeignKey(blank=True, default=None, null=True, on_delete=django.db.models.deletion.SET_DEFAULT, related_name='words', to='kab_rus_dictionary.language'),
        ),
        migrations.AddField(
            model_name='kabword',
            name='letter',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='words', to='kab_alphabet.kabletter'),
        ),
    ]
