# Generated by Django 4.1.3 on 2023-04-12 08:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0010_alter_booking_booking_code_alter_diary_entry_code_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='knowledge',
            name='status',
            field=models.CharField(choices=[('draft', 'Draft'), ('published', 'Published')], default='published', max_length=10),
        ),
        migrations.AlterField(
            model_name='booking',
            name='booking_code',
            field=models.CharField(default='F-229300A', max_length=255, unique=True),
        ),
        migrations.AlterField(
            model_name='diary',
            name='entry_code',
            field=models.CharField(default='A-216544C', max_length=255, unique=True),
        ),
    ]
