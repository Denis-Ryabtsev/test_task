import enum

from django.db import models


class OrderStatus(str, enum.Enum):
    pending = 'pending'
    ready = 'ready'
    paid = 'paid'

    @classmethod
    def choices(cls):
        return [(tag.value, tag.name.capitalize()) for tag in cls]


class Order(models.Model):
    id = models.AutoField(primary_key=True)
    table_number = models.IntegerField(
        null=False, 
        blank=False
    )
    order_cost = models.DecimalField(
        max_digits=10, 
        decimal_places=2,
        default=0
    )
    order_status = models.CharField(
        max_length=8,
        choices=OrderStatus.choices(),
        default=OrderStatus.pending.value
    )

    class Meta:
        db_table = 'orders'


class OrderDetail(models.Model):
    id = models.AutoField(primary_key=True)
    order = models.ForeignKey(
        'Order', 
        on_delete=models.CASCADE, 
        related_name='detail_order'
    )
    product_name = models.CharField(
        max_length=50,
        null=False,
        blank=False
    )
    product_price = models.DecimalField(
        max_digits=10, 
        decimal_places=2,
        default=0
    )

    class Meta:
        unique_together = ('order', 'product_name')
        db_table = 'order_details'
    