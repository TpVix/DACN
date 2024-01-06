# Generated by Django 4.2.3 on 2023-12-20 10:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0002_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='customerpurchase',
            name='customer',
        ),
        migrations.RemoveField(
            model_name='customerpurchase',
            name='orders',
        ),
        migrations.AddField(
            model_name='customerpurchase',
            name='address',
            field=models.CharField(max_length=200, null=True),
        ),
        migrations.AddField(
            model_name='customerpurchase',
            name='customer_name',
            field=models.CharField(max_length=100, null=True),
        ),
        migrations.AddField(
            model_name='customerpurchase',
            name='phone_number',
            field=models.CharField(max_length=20, null=True),
        ),
        migrations.AddField(
            model_name='customerpurchase',
            name='products',
            field=models.ManyToManyField(through='app.PurchaseItem', to='app.product'),
        ),
        migrations.AddField(
            model_name='order',
            name='transaction_id',
            field=models.CharField(max_length=200, null=True),
        ),
        migrations.AlterField(
            model_name='order',
            name='complete',
            field=models.BooleanField(default=False, null=True),
        ),
    ]