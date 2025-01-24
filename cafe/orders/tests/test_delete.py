import pytest
from django.urls import reverse
from orders.models import Order


@pytest.mark.django_db
class TestOrderDeleteAPI:
    #   Test get info about order by ID
    def test_get_order_details_success(self, api_client, create_test_data):
        order = create_test_data[0]
        url = reverse('api:api_order_delete', kwargs={'order_id': order.id})
        response = api_client.get(url)

        assert response.status_code == 200
        assert response.data['id'] == order.id
        assert response.data['table_number'] == order.table_number
        assert response.data['order_status'] == order.order_status
        assert response.data['order_cost'] == float(order.order_cost)

    #   Test get info about order, which not exists
    @pytest.mark.django_db
    def test_get_order_details_not_found(self, api_client):
        url = reverse('api:api_order_delete', kwargs={'order_id': 9999})
        response = api_client.get(url)

        assert response.status_code == 404
        assert response.data['error'] == "Order with ID 9999 does not exist."

    #   Test success delete order
    @pytest.mark.django_db
    def test_delete_order_success(self, api_client, create_test_data):
        order = create_test_data[0]
        url = reverse('api:api_order_delete', kwargs={'order_id': order.id})
        response = api_client.delete(url)

        assert response.status_code == 204
        assert Order.objects.filter(id=order.id).count() == 0

    #   Test delete order, which not exists
    @pytest.mark.django_db
    def test_delete_order_not_found(self, api_client):
        url = reverse('api:api_order_delete', kwargs={'order_id': 9999})
        response = api_client.delete(url)

        assert response.status_code == 404
        assert response.data['error'] == "Order with ID 9999 does not exist."
