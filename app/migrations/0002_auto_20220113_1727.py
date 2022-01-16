# Generated by Django 3.2.11 on 2022-01-13 14:27

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('app', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='CorrelationResult',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('first_param', models.CharField(max_length=100)),
                ('second_param', models.CharField(max_length=100)),
                ('user_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.RemoveField(
            model_name='sleeptimeperday',
            name='user_id',
        ),
        migrations.DeleteModel(
            name='AverageBloodPressure',
        ),
        migrations.DeleteModel(
            name='SleepTimePerDay',
        ),
    ]
