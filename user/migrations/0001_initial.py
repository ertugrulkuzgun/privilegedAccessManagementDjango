# Generated by Django 3.2.9 on 2021-11-22 14:12

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
            name='AuthenticationType',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('authenticationName', models.CharField(max_length=100)),
                ('ls', models.BooleanField()),
                ('cd', models.BooleanField()),
            ],
        ),
        migrations.CreateModel(
            name='CustomizeUserModel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('authType', models.IntegerField(choices=[(1, 'Full Authorized'), (2, 'Vasifsiz'), (3, 'Orta Vasifsiz'), (4, 'Orta Vasifli')])),
                ('customizedUser', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]