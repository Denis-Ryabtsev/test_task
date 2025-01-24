import pytest
from django.urls import reverse
from orders.models import Order, OrderDetail


@pytest.mark.django_db
class TestOrderAddAPI:
    #   Test get orders, when db is empty
    def test_get_orders_empty(self, api_client):
        url = reverse('api:api_order_list_create')
        response = api_client.get(url)

        assert response.status_code == 200
        assert response.data == []

    #   Test get orders
    @pytest.mark.django_db
    def test_get_orders_with_data(self, api_client, create_test_data):
        url = reverse('api:api_order_list_create')
        response = api_client.get(url)

        assert response.status_code == 200
        assert len(response.data) == 2
        assert response.data[0]['table_number'] == 1
        assert response.data[1]['table_number'] == 2

    #   Test success create order
    @pytest.mark.django_db
    def test_post_order_success(self, api_client):
        url = reverse('api:api_order_list_create')
        data = {
            "table_number": 3,
            "products": [
                {"product": "Pizza", "price": 12.0},
                {"product": "Burger", "price": 8.0}
            ]
        }
        response = api_client.post(url, data, format='json')

        assert response.status_code == 201
        assert response.data['message'] == "Order created successfully."
        assert 'order_id' in response.data

        order = Order.objects.get(id=response.data['order_id'])
        assert order.table_number == 3
        assert order.order_cost == 20.0
        assert order.detail_order.count() == 2

    #   Test create order with empty data
    @pytest.mark.django_db
    def test_post_order_missing_data(self, api_client):
        url = reverse('api:api_order_list_create')
        data = {"table_number": 3}
        response = api_client.post(url, data, format='json')

        assert response.status_code == 400
        assert response.data['error'] == "Both 'table_number' and 'products' are required."

    #   Test crate order with invalid values
    @pytest.mark.django_db
    def test_post_order_invalid_product_data(self, api_client):
        url = reverse('api:api_order_list_create')
        data = {
            "table_number": 3,
            "products": [
                {"product": "Pizza"},
            ]
        }
        response = api_client.post(url, data, format='json')

        assert response.status_code == 400
        assert response.data['error'] == "Each product must have 'product' and 'price'."
