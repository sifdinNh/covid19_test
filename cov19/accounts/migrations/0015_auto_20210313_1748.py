# Generated by Django 3.1.7 on 2021-03-13 16:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0014_auto_20210313_1703'),
    ]

    operations = [
        migrations.AlterField(
            model_name='rdv',
            name='center_id',
            field=models.IntegerField(blank=True, default=0, null=True),
        ),
    ]