# Generated by Django 3.2.6 on 2021-08-27 11:00

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Message',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('text', models.CharField(max_length=511)),
                ('user_id', models.CharField(max_length=31)),
                ('caught_pattern', models.CharField(max_length=255)),
            ],
        ),
    ]