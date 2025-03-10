# Generated by Django 5.0.4 on 2024-04-18 08:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('projects', '0002_imageaddress'),
    ]

    operations = [
        migrations.CreateModel(
            name='Block',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('index', models.IntegerField()),
                ('timestamp', models.DateTimeField(auto_now_add=True)),
                ('data', models.TextField()),
                ('previous_hash', models.CharField(max_length=64)),
                ('hash', models.CharField(max_length=64)),
                ('encrypted_data', models.TextField(blank=True, null=True)),
            ],
        ),
    ]
