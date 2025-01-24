import pytest
from rest_framework.test import APIClient
from orders.models import Order, OrderDetail


@pytest.fixture
def api_client():
    return APIClient()


@pytest.fixture
@pytest.mark.django_db
def create_test_data():
    order1 = Order.objects.create(table_number=1, order_cost=20.0, order_status="paid")
    order2 = Order.objects.create(table_number=2, order_cost=30.0, order_status="pending")

    OrderDetail.objects.create(order=order1, product_name="Pizza", product_price=10.0)
    OrderDetail.objects.create(order=order1, product_name="Burger", product_price=10.0)
    OrderDetail.objects.create(order=order2, product_name="Fries", product_price=30.0)

    return [order1, order2]
