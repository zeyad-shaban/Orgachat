# Generated by Django 3.1.2 on 2020-10-29 17:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('metrics', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='GrowthReport',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('hypo', models.CharField(max_length=70)),
                ('messages_per_day', models.IntegerField()),
                ('repeat_rate', models.IntegerField()),
                ('new_users_per_day', models.IntegerField()),
                ('date', models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.DeleteModel(
            name='GrothReport',
        ),
    ]
