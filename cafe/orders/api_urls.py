from django.urls import path

from orders.views import (
    APIRoot,
    OrderAddAPI,
    OrderChangeAPI,
    OrderChangeStatusAPI,
    OrderSearchAPI, 
    TotalAmountAPI, 
    OrderDeleteAPI
)


urlpatterns = [
    path('', APIRoot.as_view(), name='api_root'),
    path('orders/', OrderAddAPI.as_view(), name='api_order_list_create'),
    path('orders/<int:order_id>/delete/', OrderDeleteAPI.as_view(), name='api_order_delete'),
    path('orders/change-status/', OrderChangeStatusAPI.as_view(), name='api_order_change_status'),
    path('orders/search/', OrderSearchAPI.as_view(), name='api_order_search'),
    path('orders/total/', TotalAmountAPI.as_view(), name='api_order_total'),
    path('orders/<int:order_id>/edit/', OrderChangeAPI.as_view(), name='api_order_change')
]