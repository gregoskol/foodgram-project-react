# Generated by Django 2.2.16 on 2023-02-13 14:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='password',
            field=models.CharField(blank=True, max_length=150, verbose_name='Пароль'),
        ),
    ]