import pytest
from django.urls import reverse


@pytest.mark.django_db
class TestOrderSearchAPI:
    #   Test search order by number table
    def test_search_orders_by_table_number(self, api_client, create_test_data):
        url = reverse('api:api_order_search')
        params = {"table_number": 1}
        response = api_client.get(url, params)

        assert response.status_code == 200
        assert len(response.data) == 1
        assert response.data[0]['table_number'] == 1

    #   Test search order by status
    @pytest.mark.django_db
    def test_search_orders_by_status(self, api_client, create_test_data):
        url = reverse('api:api_order_search')
        params = {"status": "paid"}
        response = api_client.get(url, params)

        assert response.status_code == 200
        assert len(response.data) == 1
        assert response.data[0]['order_status'] == "paid"

    #   Test search order by table name and status
    @pytest.mark.django_db
    def test_search_orders_by_table_number_and_status(self, api_client, create_test_data):
        url = reverse('api:api_order_search')
        params = {"table_number": 1, "status": "paid"}
        response = api_client.get(url, params)

        assert response.status_code == 200
        assert len(response.data) == 1
        assert response.data[0]['table_number'] == 1
        assert response.data[0]['order_status'] == "paid"

    #   Test search order. which not exists by input values
    @pytest.mark.django_db
    def test_search_orders_no_results(self, api_client):
        url = reverse('api:api_order_search')
        params = {"table_number": 999, "status": "nonexistent"}
        response = api_client.get(url, params)

        assert response.status_code == 200
        assert len(response.data) == 0
