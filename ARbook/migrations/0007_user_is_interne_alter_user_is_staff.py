# Generated by Django 4.1.2 on 2023-04-26 11:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ARbook', '0006_alter_alr_bloc_alter_basicmoves_perfusion'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='is_interne',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='user',
            name='is_staff',
            field=models.BooleanField(default=False),
        ),
    ]
