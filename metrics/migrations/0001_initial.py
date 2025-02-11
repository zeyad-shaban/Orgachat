# Generated by Django 3.1.3 on 2020-11-30 09:09

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='GrowthReport',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateTimeField(auto_now_add=True)),
                ('hypo', models.CharField(max_length=70)),
                ('desc', models.TextField(blank=True, null=True)),
                ('effort', models.CharField(choices=[('easy', 'easy < 2 day'), ('medium', 'medium > 2day > 4 days'), ('hard', 'hard > 4 days')], max_length=70)),
                ('repeat_rate', models.FloatField()),
                ('messages_per_user', models.FloatField()),
                ('new_users_per_day', models.FloatField()),
            ],
        ),
    ]
