import pytest
from django.urls import reverse
from orders.models import Order, OrderDetail


@pytest.mark.django_db
class TestOrderChangeAPI:
    #   Test delete product from order
    def test_delete_product_success(self, api_client, create_test_data):
        order = create_test_data[0]
        url = reverse('api:api_order_change', kwargs={'order_id': order.id})
        data = {
            "product_name": "Pizza"
        }

        response = api_client.delete(url, data, format='json')

        assert response.status_code == 204
        assert not OrderDetail.objects.filter(order=order, product_name="Pizza").exists()

        order.refresh_from_db()
        assert order.order_cost == 10.0

    #   Test delete product, which not exists in order
    @pytest.mark.django_db
    def test_delete_product_not_found(self, api_client, create_test_data):
        order = create_test_data[0]
        url = reverse('api:api_order_change', kwargs={'order_id': order.id})
        data = {
            "product_name": "Nonexistent"
        }

        response = api_client.delete(url, data, format='json')

        assert response.status_code == 404
        assert response.data['error'] == "Product Nonexistent does not exist in this order."
