from django.urls import path

from orders.views import (
    APIRootHTML,
    OrderAddHTML,
    OrderChangeHTML,
    OrderChangeStatusHTML, 
    OrderSearchHTML, 
    TotalAmountHTML,
    OrderDeleteHTML    
)

urlpatterns = [
    path('', APIRootHTML.as_view(), name='html_api_root'),
    path('orders/', OrderAddHTML.as_view(), name='html_order_list'),
    path('orders/delete/', OrderDeleteHTML.as_view(), name='html_order_delete'),
    path('orders/change-status/', OrderChangeStatusHTML.as_view(), name='html_order_change_status'),
    path('orders/search/', OrderSearchHTML.as_view(), name='html_order_search'),
    path('orders/total/', TotalAmountHTML.as_view(), name='html_order_total'),
    path('orders/change/', OrderChangeHTML.as_view(), name='html_order_change')
]