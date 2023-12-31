# Generated by Django 4.1.3 on 2023-04-08 12:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0003_alter_booking_booking_code_alter_diary_entry_code_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='booking',
            name='booking_code',
            field=models.CharField(default='T-790499Z', max_length=255, unique=True),
        ),
        migrations.AlterField(
            model_name='diary',
            name='entry_code',
            field=models.CharField(default='R-186005Y', max_length=255, unique=True),
        ),
        migrations.AlterField(
            model_name='snippetcategory',
            name='title',
            field=models.CharField(default='all', max_length=100, unique=True),
        ),
    ]
