# Generated by Django 5.1.5 on 2025-01-29 11:04

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('core', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='TourInfo',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('tour_type', models.CharField(choices=[('twohour', 'Two Hour Tour'), ('threehour', 'Three Hour Tour')], max_length=15, verbose_name='Tour Type')),
                ('order', models.PositiveIntegerField(verbose_name='Order')),
                ('place_name', models.CharField(max_length=255, verbose_name='Place Name (English)')),
                ('description', models.TextField(verbose_name='Description (English)')),
                ('voice_path', models.FileField(blank=True, null=True, upload_to='voices/en/', verbose_name='Voice Path (English)')),
                ('google_maps_url', models.URLField(max_length=5000, verbose_name='Google Maps URL')),
                ('info_url', models.URLField(verbose_name='Info URL')),
            ],
            options={
                'verbose_name': 'Tour Info',
                'verbose_name_plural': 'Tour Infos',
                'ordering': ['order'],
            },
        ),
        migrations.CreateModel(
            name='TourInfoTranslation',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('place_name', models.CharField(max_length=255, verbose_name='Place Name')),
                ('description', models.TextField(blank=True, null=True, verbose_name='Description')),
                ('voice_path', models.FileField(blank=True, null=True, upload_to='voices/', verbose_name='Voice Path')),
                ('info_url', models.URLField(verbose_name='Info URL')),
                ('language', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='core.languagesetting', verbose_name='Language')),
                ('tour_info', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='translations', to='tour.tourinfo', verbose_name='Tour Info')),
            ],
            options={
                'verbose_name': 'Tour Info Translation',
                'verbose_name_plural': 'Tour Info Translations',
                'unique_together': {('tour_info', 'language')},
            },
        ),
    ]
