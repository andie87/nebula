# Generated by Django 3.1.8 on 2021-04-21 07:33

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Consumer',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('apikey', models.CharField(max_length=32)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Api',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=128, unique=True)),
                ('request_path', models.CharField(max_length=255)),
                ('upstream_url', models.CharField(max_length=255)),
                ('plugin', models.IntegerField(choices=[(0, 'Remote auth'), (1, 'Basic auth'), (2, 'Key auth'), (3, 'Server auth')], default=0)),
                ('consumers', models.ManyToManyField(blank=True, to='apigateway.Consumer')),
            ],
        ),
    ]
