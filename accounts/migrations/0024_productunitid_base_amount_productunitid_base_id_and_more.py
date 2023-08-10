# Generated by Django 4.1.3 on 2023-05-24 12:45

from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0023_productunitid_product_alert_max_stock_number_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='productunitid',
            name='base_amount',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=10),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='productunitid',
            name='base_id',
            field=models.IntegerField(default=1),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='productunitid',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True, default=django.utils.timezone.now),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='productunitid',
            name='delete_description',
            field=models.TextField(null=True),
        ),
        migrations.AddField(
            model_name='productunitid',
            name='description',
            field=models.TextField(default='test'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='productunitid',
            name='fk_cashier_create_id',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.DO_NOTHING, related_name='product_unit_id_cashier_created', to='accounts.cashier'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='productunitid',
            name='fk_cashier_update_id',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.DO_NOTHING, related_name='product_unit_id_cashier_updated', to='accounts.cashier'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='productunitid',
            name='is_deleted',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='productunitid',
            name='name',
            field=models.CharField(default='test', max_length=50),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='productunitid',
            name='no',
            field=models.IntegerField(default=1),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='productunitid',
            name='symbol',
            field=models.CharField(default='1', max_length=10),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='productunitid',
            name='updated_at',
            field=models.DateTimeField(auto_now=True),
        ),
        migrations.AlterField(
            model_name='booking',
            name='booking_code',
            field=models.CharField(default='O-955919H', max_length=255, unique=True),
        ),
        migrations.AlterField(
            model_name='closure',
            name='closure_unique_id',
            field=models.UUIDField(verbose_name=uuid.UUID('de519b5d-3039-46a4-95a8-2082c1af9255')),
        ),
        migrations.AlterField(
            model_name='diary',
            name='entry_code',
            field=models.CharField(default='Z-638857K', max_length=255, unique=True),
        ),
    ]
