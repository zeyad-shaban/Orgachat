# Generated by Django 3.1.3 on 2020-12-02 05:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='password',
            field=models.TextField(blank=True, null=True),
        ),
    ]
