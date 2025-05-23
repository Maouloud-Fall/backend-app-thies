# Generated by Django 5.2.1 on 2025-05-16 14:40

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Resource',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=255, verbose_name='Titre')),
                ('slug', models.SlugField(blank=True, help_text='Ce champ est généré automatiquement à partir du titre', max_length=255, unique=True, verbose_name='Slug (URL)')),
                ('content', models.TextField(verbose_name='Contenu')),
                ('category', models.CharField(choices=[('formation', 'Formation'), ('orientation', 'Orientation'), ('actualités', 'Actualités'), ('conseils', 'Conseils')], max_length=20, verbose_name='Catégorie')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Date de création')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='Date de modification')),
                ('is_published', models.BooleanField(default=True, verbose_name='Publié')),
            ],
            options={
                'verbose_name': 'Ressource',
                'verbose_name_plural': 'Ressources',
                'ordering': ['-created_at'],
                'indexes': [models.Index(fields=['category'], name='resources_r_categor_8e2710_idx'), models.Index(fields=['created_at'], name='resources_r_created_215cda_idx'), models.Index(fields=['slug'], name='resources_r_slug_1bd26a_idx')],
            },
        ),
    ]
