# Generated by Django 5.1.5 on 2025-01-23 16:13

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Order',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('table_number', models.IntegerField()),
                ('order_cost', models.DecimalField(decimal_places=2, default=0, max_digits=10)),
                ('order_status', models.CharField(choices=[('pending', 'Pending'), ('ready', 'Ready'), ('paid', 'Paid')], default='pending', max_length=8)),
            ],
            options={
                'db_table': 'orders',
            },
        ),
        migrations.CreateModel(
            name='OrderDetail',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('product_name', models.CharField(max_length=50)),
                ('product_price', models.DecimalField(decimal_places=2, default=0, max_digits=10)),
                ('order', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='detail_order', to='orders.order')),
            ],
            options={
                'db_table': 'order_details',
                'unique_together': {('order', 'product_name')},
            },
        ),
    ]
