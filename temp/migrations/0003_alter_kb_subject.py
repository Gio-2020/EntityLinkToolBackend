# Generated by Django 4.1 on 2022-11-15 14:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('temp', '0002_kb_delete_testmodel'),
    ]

    operations = [
        migrations.AlterField(
            model_name='kb',
            name='subject',
            field=models.CharField(max_length=100, verbose_name='名称'),
        ),
    ]
