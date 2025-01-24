import pytest
from django.urls import reverse
from orders.models import Order, OrderStatus


@pytest.mark.django_db
class TestOrderChangeStatusAPI:
    #   Test access change order's status
    def test_change_status_success(self, api_client, create_test_data):
        order = create_test_data[0]
        url = reverse('api:api_order_change_status')
        data = {
            "order_id": order.id,
            "status": "pending"
        }

        response = api_client.patch(url, data, format='json')

        assert response.status_code == 200
        assert response.data['message'] == f"Order with ID {order.id} was successfully updated to status 'pending'."

        order.refresh_from_db()
        assert order.order_status == "pending"

    #   Test change order's status without input ID
    @pytest.mark.django_db
    def test_change_status_missing_order_id(self, api_client):
        url = reverse('api:api_order_change_status')
        data = {
            "status": "paid"
        }

        response = api_client.patch(url, data, format='json')

        assert response.status_code == 400
        assert response.data['error'] == "Order ID is required."

    #   Test change order's status without input status
    @pytest.mark.django_db
    def test_change_status_missing_status(self, api_client, create_test_data):
        order = create_test_data[0]
        url = reverse('api:api_order_change_status')
        data = {
            "order_id": order.id
        }

        response = api_client.patch(url, data, format='json')

        assert response.status_code == 400
        assert response.data['error'] == "New status is required."

    #   Test change status of order, which not exists
    @pytest.mark.django_db
    def test_change_status_invalid_order_id(self, api_client):
        url = reverse('api:api_order_change_status')
        data = {
            "order_id": 9999,
            "status": "paid"
        }

        response = api_client.patch(url, data, format='json')

        assert response.status_code == 404
        assert response.data['error'] == "Order with ID 9999 does not exist."

    #   Test change status with invalid ID
    @pytest.mark.django_db
    def test_change_status_invalid_status(self, api_client, create_test_data):
        order = create_test_data[0]
        url = reverse('api:api_order_change_status')
        data = {
            "order_id": order.id,
            "status": "invalid_status"
        }

        response = api_client.patch(url, data, format='json')

        assert response.status_code == 400
        assert response.data['error'] == "Invalid status 'invalid_status'."
