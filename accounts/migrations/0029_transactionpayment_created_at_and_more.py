# Generated by Django 4.1.3 on 2023-05-24 13:52

from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0028_transactionpaymenttemp_fk_transaction_head_id_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='transactionpayment',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True, default=django.utils.timezone.now),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='transactionpayment',
            name='currency_code',
            field=models.IntegerField(default=1),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='transactionpayment',
            name='currency_exchange_rate',
            field=models.DecimalField(decimal_places=2, default=1, max_digits=10),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='transactionpayment',
            name='currency_total',
            field=models.DecimalField(decimal_places=2, default=1, max_digits=10),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='transactionpayment',
            name='delete_description',
            field=models.TextField(null=True),
        ),
        migrations.AddField(
            model_name='transactionpayment',
            name='fk_cashier_create_id',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.DO_NOTHING, related_name='transaction_head1_cashier_created_id', to='accounts.cashier'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='transactionpayment',
            name='fk_cashier_update_id',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.DO_NOTHING, related_name='transaction_head1_cashier_updated_id', to='accounts.cashier'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='transactionpayment',
            name='fk_transaction_head_id',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.DO_NOTHING, related_name='transaction_head1_id', to='accounts.transactionhead'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='transactionpayment',
            name='installment_count',
            field=models.IntegerField(default=1),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='transactionpayment',
            name='is_cancel',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='transactionpayment',
            name='is_deleted',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='transactionpayment',
            name='line_no',
            field=models.IntegerField(default=1),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='transactionpayment',
            name='payment_tool_id',
            field=models.CharField(max_length=50, null=True),
        ),
        migrations.AddField(
            model_name='transactionpayment',
            name='payment_total',
            field=models.DecimalField(decimal_places=2, default=1, max_digits=10),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='transactionpayment',
            name='payment_type',
            field=models.CharField(default=1, max_length=50),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='transactionpayment',
            name='updated_at',
            field=models.DateTimeField(auto_now=True),
        ),
        migrations.AlterField(
            model_name='booking',
            name='booking_code',
            field=models.CharField(default='M-219386K', max_length=255, unique=True),
        ),
        migrations.AlterField(
            model_name='closure',
            name='closure_unique_id',
            field=models.UUIDField(verbose_name=uuid.UUID('bb397c78-e020-4628-b5e3-8a7db1ad2794')),
        ),
        migrations.AlterField(
            model_name='diary',
            name='entry_code',
            field=models.CharField(default='K-857200E', max_length=255, unique=True),
        ),
        migrations.AlterField(
            model_name='transactionhead',
            name='transaction_unique_id',
            field=models.URLField(verbose_name=uuid.UUID('7fe3140a-65ce-4b5b-8757-7b1718a01317')),
        ),
        migrations.AlterField(
            model_name='transactionheadtemp',
            name='transaction_unique_id',
            field=models.URLField(verbose_name=uuid.UUID('5623567f-40fd-4b7c-9ea2-31e05f1f86f4')),
        ),
    ]
