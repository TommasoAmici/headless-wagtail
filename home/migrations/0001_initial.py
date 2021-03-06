# Generated by Django 4.0.2 on 2022-02-25 15:09

from django.db import migrations, models
import django.db.models.deletion
import home.blocks
import wagtail.core.fields
import wagtail.images.blocks


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('wagtailcore', '0066_collection_management_permissions'),
    ]

    operations = [
        migrations.CreateModel(
            name='ArticlePage',
            fields=[
                ('page_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='wagtailcore.page')),
                ('summary', models.CharField(max_length=300)),
                ('body', wagtail.core.fields.StreamField([('paragraph', home.blocks.CustomRichTextBlock()), ('image', wagtail.images.blocks.ImageChooserBlock(icon='image'))])),
            ],
            options={
                'abstract': False,
            },
            bases=('wagtailcore.page',),
        ),
    ]
