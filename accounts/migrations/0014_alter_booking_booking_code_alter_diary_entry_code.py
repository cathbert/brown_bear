# Generated by Django 4.1.3 on 2023-04-12 13:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0013_alter_booking_booking_code_alter_diary_entry_code'),
    ]

    operations = [
        migrations.AlterField(
            model_name='booking',
            name='booking_code',
            field=models.CharField(default='X-624345S', max_length=255, unique=True),
        ),
        migrations.AlterField(
            model_name='diary',
            name='entry_code',
            field=models.CharField(default='E-576750C', max_length=255, unique=True),
        ),
    ]
