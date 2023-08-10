# Generated by Django 4.1.3 on 2023-05-24 14:09

from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0030_transactionproducttemp_created_at_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='transactionproduct',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True, default=django.utils.timezone.now),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='transactionproduct',
            name='delete_description',
            field=models.TextField(null=True),
        ),
        migrations.AddField(
            model_name='transactionproduct',
            name='fk_cashier_create_id',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.DO_NOTHING, related_name='product_1_product_temp_cashier_created', to='accounts.cashier'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='transactionproduct',
            name='fk_cashier_update_id',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.DO_NOTHING, related_name='product_1_product_temp_cashier_updated', to='accounts.cashier'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='transactionproduct',
            name='fk_department_main_group_id',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.DO_NOTHING, related_name='product_department_main_grp', to='accounts.departmentmaingroup'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='transactionproduct',
            name='fk_department_sub_group_id',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='product_department_subgrp_id', to='accounts.departmentsubgroup'),
        ),
        migrations.AddField(
            model_name='transactionproduct',
            name='fk_product_barcode_id',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='product_broduct_barcode_1', to='accounts.productbarcode'),
        ),
        migrations.AddField(
            model_name='transactionproduct',
            name='fk_product_barcode_mask_id',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='product_product_barcode_mask_1', to='accounts.productbarcodemask'),
        ),
        migrations.AddField(
            model_name='transactionproduct',
            name='fk_product_id',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='product_transaction_product_id', to='accounts.product'),
        ),
        migrations.AddField(
            model_name='transactionproduct',
            name='fk_transaction_head_id',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.DO_NOTHING, related_name='transaction_head_ident', to='accounts.transactionhead'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='transactionproduct',
            name='is_cancel',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='transactionproduct',
            name='is_deleted',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='transactionproduct',
            name='line_no',
            field=models.IntegerField(default=1),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='transactionproduct',
            name='total_discount',
            field=models.DecimalField(decimal_places=2, default=1, max_digits=10),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='transactionproduct',
            name='total_price',
            field=models.DecimalField(decimal_places=2, default=1, max_digits=10),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='transactionproduct',
            name='total_vat',
            field=models.DecimalField(decimal_places=2, default=1, max_digits=10),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='transactionproduct',
            name='unit_discount',
            field=models.DecimalField(decimal_places=2, default=1, max_digits=10),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='transactionproduct',
            name='unit_price',
            field=models.DecimalField(decimal_places=2, default=1, max_digits=10),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='transactionproduct',
            name='updated_at',
            field=models.DateTimeField(auto_now=True),
        ),
        migrations.AddField(
            model_name='transactionproduct',
            name='vat_rate',
            field=models.IntegerField(default=1),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='booking',
            name='booking_code',
            field=models.CharField(default='W-396005E', max_length=255, unique=True),
        ),
        migrations.AlterField(
            model_name='closure',
            name='closure_unique_id',
            field=models.UUIDField(verbose_name=uuid.UUID('f89d345c-af02-49b5-850c-0ec8b48842e1')),
        ),
        migrations.AlterField(
            model_name='diary',
            name='entry_code',
            field=models.CharField(default='L-573577E', max_length=255, unique=True),
        ),
        migrations.AlterField(
            model_name='transactionhead',
            name='transaction_unique_id',
            field=models.URLField(verbose_name=uuid.UUID('215cc6a7-08b1-4e7a-b979-7f33b5fb6b2c')),
        ),
        migrations.AlterField(
            model_name='transactionheadtemp',
            name='transaction_unique_id',
            field=models.URLField(verbose_name=uuid.UUID('8b5271fe-f828-4de6-88e0-a6e4d72b89bf')),
        ),
    ]