# Generated by Django 3.1.7 on 2021-03-09 21:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0010_auto_20210309_2127'),
    ]

    operations = [
        migrations.RenameField(
            model_name='rdv',
            old_name='is_pass',
            new_name='is_confirmed',
        ),
        migrations.AddField(
            model_name='rdv',
            name='is_rejected',
            field=models.BooleanField(default=False),
        ),
    ]