import pytest
from django.urls import reverse

from orders.models import Order, OrderDetail


@pytest.mark.django_db
class TestTotalAmountAPI:
    #   Test count cost of order with status = paid
    def test_total_amount_paid_orders(self, api_client, create_test_data):
        url = reverse('api:api_order_total')
        response = api_client.get(url)

        assert response.status_code == 200
        assert response.data['total'] == 20.0

    #   Test count cost of order, when status = paid not exists in db
    @pytest.mark.django_db
    def test_total_amount_no_paid_orders(self, api_client):
        Order.objects.all().update(order_status="pending")

        url = reverse('api:api_order_total')
        response = api_client.get(url)

        assert response.status_code == 200
        assert response.data['total'] == 0 
