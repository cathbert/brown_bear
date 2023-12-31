# Generated by Django 4.1.3 on 2023-05-24 14:22

from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0033_transactiontotal_created_at_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='vat',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True, default=django.utils.timezone.now),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='vat',
            name='delete_description',
            field=models.TextField(null=True),
        ),
        migrations.AddField(
            model_name='vat',
            name='description',
            field=models.TextField(null=True),
        ),
        migrations.AddField(
            model_name='vat',
            name='fk_cashier_create_id',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.DO_NOTHING, related_name='vat_currency_cashier_created_id', to='accounts.cashier'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='vat',
            name='fk_cashier_update_id',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.DO_NOTHING, related_name='vat_currency_cashier_updated_id', to='accounts.cashier'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='vat',
            name='is_deleted',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='vat',
            name='name',
            field=models.CharField(default=1, max_length=50),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='vat',
            name='no',
            field=models.IntegerField(default=1),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='vat',
            name='rate',
            field=models.IntegerField(default=1),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='vat',
            name='updated_at',
            field=models.DateTimeField(auto_now=True),
        ),
        migrations.AlterField(
            model_name='booking',
            name='booking_code',
            field=models.CharField(default='V-41927A', max_length=255, unique=True),
        ),
        migrations.AlterField(
            model_name='closure',
            name='closure_unique_id',
            field=models.UUIDField(verbose_name=uuid.UUID('6923bac2-1fec-4d43-8d04-a011155e4bc6')),
        ),
        migrations.AlterField(
            model_name='diary',
            name='entry_code',
            field=models.CharField(default='H-394468D', max_length=255, unique=True),
        ),
        migrations.AlterField(
            model_name='transactionhead',
            name='transaction_unique_id',
            field=models.URLField(verbose_name=uuid.UUID('c869c03c-3fec-4afa-b61d-d0fb982fdbc7')),
        ),
        migrations.AlterField(
            model_name='transactionheadtemp',
            name='transaction_unique_id',
            field=models.URLField(verbose_name=uuid.UUID('e306caa6-13d4-49d5-8b3b-dc549d840619')),
        ),
    ]
