# Generated by Django 4.0 on 2021-12-17 14:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0002_alter_daligate_id_alter_exist_id_alter_location_id_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='meeting',
            name='meeting_end_detail',
            field=models.DateTimeField(blank=True, null=True),
        ),
    ]