# Generated by Django 4.1.3 on 2023-05-24 13:01

from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0024_productunitid_base_amount_productunitid_base_id_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='TransactionDiscount',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
            ],
        ),
        migrations.CreateModel(
            name='TransactionHead',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
            ],
        ),
        migrations.CreateModel(
            name='TransactionHeadTemp',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
            ],
        ),
        migrations.CreateModel(
            name='TransactionPayment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
            ],
        ),
        migrations.CreateModel(
            name='TransactionPaymentTemp',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
            ],
        ),
        migrations.CreateModel(
            name='TransactionProduct',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
            ],
        ),
        migrations.CreateModel(
            name='TransactionProductTemp',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
            ],
        ),
        migrations.CreateModel(
            name='TransactionTotal',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
            ],
        ),
        migrations.CreateModel(
            name='TransactionTotalTemp',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
            ],
        ),
        migrations.AlterField(
            model_name='booking',
            name='booking_code',
            field=models.CharField(default='C-626590S', max_length=255, unique=True),
        ),
        migrations.AlterField(
            model_name='closure',
            name='closure_unique_id',
            field=models.UUIDField(verbose_name=uuid.UUID('f4d8390d-77b3-48e7-b028-83e3a92e6891')),
        ),
        migrations.AlterField(
            model_name='diary',
            name='entry_code',
            field=models.CharField(default='H-800473H', max_length=255, unique=True),
        ),
        migrations.CreateModel(
            name='TransactionDiscountTemp',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('line_no', models.IntegerField()),
                ('discount_type', models.CharField(max_length=50)),
                ('discount_amount', models.DecimalField(decimal_places=2, max_digits=10)),
                ('discount_rate', models.DecimalField(decimal_places=2, max_digits=10, null=True)),
                ('discount_code', models.CharField(max_length=15, null=True)),
                ('is_cancel', models.BooleanField(default=False)),
                ('is_deleted', models.BooleanField(default=False)),
                ('delete_description', models.TextField(null=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('fk_cashier_create_id', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, related_name='transaction_dicount_temp_cashier_created', to='accounts.cashier')),
                ('fk_cashier_update_id', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, related_name='transaction_dicount_temp_cashier_updated', to='accounts.cashier')),
                ('fk_transaction_head_id', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, related_name='transaction_dicount_temp_head', to='accounts.transactionheadtemp')),
                ('fk_transaction_payment_id', models.ForeignKey(null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='transaction_dicount_temp_payment', to='accounts.transactionpaymenttemp')),
                ('fk_transaction_product_id', models.ForeignKey(null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='transaction_dicount_temp_product', to='accounts.transactionproducttemp')),
                ('fk_transaction_total_id', models.ForeignKey(null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='transaction_dicount_temp_total', to='accounts.transactiontotaltemp')),
            ],
        ),
    ]
