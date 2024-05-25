# Generated by Django 5.0.6 on 2024-05-25 16:57

import taggit.managers
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0003_article_tags'),
        ('taggit', '0006_rename_taggeditem_content_type_object_id_taggit_tagg_content_8fc721_idx'),
    ]

    operations = [
        migrations.AlterField(
            model_name='article',
            name='tags',
            field=taggit.managers.TaggableManager(help_text='Select tag', through='taggit.TaggedItem', to='taggit.Tag', verbose_name='Tags'),
        ),
    ]
