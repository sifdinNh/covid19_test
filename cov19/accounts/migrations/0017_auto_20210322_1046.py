# Generated by Django 3.1.7 on 2021-03-22 09:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0016_citoyen_is_rdv'),
    ]

    operations = [
        migrations.AlterField(
            model_name='citoyen',
            name='RAMID',
            field=models.CharField(blank=True, default=0, max_length=10, null=True),
        ),
    ]
