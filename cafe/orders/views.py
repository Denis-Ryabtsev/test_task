from django.shortcuts import get_object_or_404, render, redirect
from django.db.models import Sum
from django.urls import reverse
from django.views import View
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from orders.models import (
    Order, 
    OrderDetail, 
    OrderStatus
)
from orders.serializers import  OrderSerializer


#   View for API. Class include methods for get list orders and add new order  
class OrderAddAPI(APIView):
    #   Get list orders
    def get(self, request):
        #   Get all orders from table 'orders' and apply the required data format
        orders = Order.objects.all()
        serializer = OrderSerializer(orders, many=True)

        return Response(
            serializer.data, 
            status=status.HTTP_200_OK
        )
    
    #   Add new order
    def post(self, request):
        #   Get the input data from client request
        table_number = request.data.get('table_number')
        products_data = request.data.get('products')

        #   Checking data for emptiness
        if not table_number or not products_data:
            return Response(
                {'error': "Both 'table_number' and 'products' are required."},
                status=status.HTTP_400_BAD_REQUEST
            )
        #   Creating order with temp 'order_cost'
        order = Order.objects.create(
            table_number=table_number,
            order_cost=0
        )

        total_cost = 0
        #   Check invalid input data format and creating record in order_detail's table
        for product_data in products_data:
            product_name = product_data.get('product')
            product_price = product_data.get('price')
            
            if not product_name or product_price is None:
                return Response(
                    {'error': "Each product must have 'product' and 'price'."},
                    status=status.HTTP_400_BAD_REQUEST
                )
            
            total_cost += product_price
            OrderDetail.objects.create(
                order=order, 
                product_name=product_name,
                product_price=product_price
            )
        #   Save the order with final anmount
        order.order_cost = total_cost
        order.save()

        return Response(
            {'message': "Order created successfully.", "order_id": order.id},
            status=status.HTTP_201_CREATED
        )


#   View for HTML page. Same as the API view (OrderAddAPI)
class OrderAddHTML(View):
    def get(self, request):
        orders = Order.objects.prefetch_related('detail_order').all()
        
        return render(
            request, 
            'orders/order_list.html', 
            {'orders': orders}
        )

    def post(self, request):
        table_number = request.POST.get('table_number')
        product_names = request.POST.getlist('products[][product]')
        product_prices = request.POST.getlist('products[][price]')

        if not table_number or not product_names or not product_prices:
            return render(
                request,
                'orders/order_list.html',
                {
                    'error': "Both 'table_number' and products are required.", 
                    'orders': Order.objects.all()
                }
            )

        try:
            table_number = int(table_number)
        except ValueError:
            return render(
                request,
                'orders/order_list.html',
                {
                    'error': "Table number must be a valid number.", 
                    'orders': Order.objects.all()
                }
            )

        order = Order.objects.create(
            table_number=table_number,
            order_cost=0
        )

        total_cost = 0

        for name, price in zip(product_names, product_prices):
            if not name or not price:
                return render(
                    request,
                    'orders/order_list.html',
                    {
                        'error': "Each product must have a name and a price.", 
                        'orders': Order.objects.all()
                    }
                )
            
            total_cost += float(price)
            OrderDetail.objects.create(
                order=order,
                product_name=name,
                product_price=price
            )

        order.order_cost = total_cost
        order.save()

        return redirect('html:html_order_list')


#   View for API. Class include methods for change order's status 
class OrderChangeStatusAPI(APIView):
    def patch(self, request):
        #   Get the input data from client request
        order_id = request.data.get('order_id')
        new_status = request.data.get('status')

        #   Checking data for emptiness
        if not order_id:
            return Response(
                {'error': 'Order ID is required.'},
                status=status.HTTP_400_BAD_REQUEST
            )
        if not new_status:
            return Response(
                {'error': 'New status is required.'},
                status=status.HTTP_400_BAD_REQUEST
            )

        #   Checking for existence of order with input ID
        try:
            order = Order.objects.get(pk=order_id)
        except Order.DoesNotExist:
            return Response(
                {'error': f"Order with ID {order_id} does not exist."},
                status=status.HTTP_404_NOT_FOUND
            )

        #   Checking valid format of input status
        if new_status not in dict(OrderStatus.choices()).keys():
            return Response(
                {'error': f"Invalid status '{new_status}'."},
                status=status.HTTP_400_BAD_REQUEST
            )

        #   Update order's status
        order.order_status = new_status
        order.save()

        return Response(
            {
                'message': f"Order with ID {order_id} was successfully"
                            f" updated to status '{new_status}'."
            },
            status=status.HTTP_200_OK
        )


#   View for HTML page. Same as the API view (OrderChangeStatusAPI)
class OrderChangeStatusHTML(View):
    def get(self, request):

        return render(
            request, 
            'orders/order_change_status.html', 
            {
                'order_status_choices': OrderStatus.choices()
            }
        )

    def post(self, request):
        order_id = request.POST.get('order_id')
        new_status = request.POST.get('status')

        if not order_id:
            return render(
                request, 
                'orders/order_change_status.html', 
                {
                    'error': 'Order ID is required.',
                    'order_status_choices': OrderStatus.choices()
                }
            )

        if not new_status:
            return render(
                request, 
                'orders/order_change_status.html', 
                {
                    'error': 'New status is required.',
                    'order_status_choices': OrderStatus.choices()
                }
            )

        try:
            order = Order.objects.get(pk=order_id)
        except Order.DoesNotExist:
            return render(
                request, 
                'orders/order_change_status.html', 
                {
                    'error': f"Order with ID {order_id} does not exist.",
                    'order_status_choices': OrderStatus.choices()
                }
            )

        if new_status not in dict(OrderStatus.choices()).keys():
            return render(
                request, 
                'orders/order_change_status.html', 
                {
                    'error': f"Invalid status '{new_status}'.",
                    'order_status_choices': OrderStatus.choices()
                }
            )

        order.order_status = new_status
        order.save()

        return render(
            request, 
            'orders/order_change_status.html', 
            {
                'success': f"Order with ID {order_id} was successfully" 
                            f"updated to status '{new_status}'.",
                'order_status_choices': OrderStatus.choices()
            }
        )


#   View for API. Class include methods for orders  
class OrderDeleteAPI(APIView):
    #   Get order, which will deleted
    def get(self, request, order_id):
        #   Get order, having input ID
        try:
            order = Order.objects.get(pk=order_id)
        except Order.DoesNotExist:
            return Response(
                {'error': f"Order with ID {order_id} does not exist."},
                status=status.HTTP_404_NOT_FOUND
            )

        return Response(
            {
                'id': order.id,
                'table_number': order.table_number,
                'order_status': order.order_status,
                'order_cost': order.order_cost
            },
            status=status.HTTP_200_OK
        )

    #   Delete order, having input ID
    def delete(self, request, order_id):
        
        try:
            order = Order.objects.get(pk=order_id)
        except Order.DoesNotExist:
            return Response(
                {'error': f"Order with ID {order_id} does not exist."},
                status=status.HTTP_404_NOT_FOUND
            )

        #   Delete record from db
        order.delete()
        return Response(
            {'message': f"Order with ID {order_id} was successfully deleted."},
            status=status.HTTP_204_NO_CONTENT
        )


#   View for HTML page. Same as the API view (OrderDeleteAPI)
class OrderDeleteHTML(View):
    def get(self, request):
        return render(
            request, 
            'orders/order_delete.html'
        )

    def post(self, request):
        order_id = request.POST.get('order_id')

        if not order_id:
            return render(
                request, 
                'orders/order_delete.html', 
                {
                    'error': 'Order ID is required.',
                }
            )

        try:
            order = Order.objects.get(pk=order_id)
        except Order.DoesNotExist:
            return render(
                request, 
                'orders/order_delete.html', 
                {
                    'error': f"Order with ID {order_id} does not exist.",
                }
            )

        order.delete()
        return render(
            request, 
            'orders/order_delete.html', 
            {
                'success': f"Order with ID {order_id} was successfully deleted.",
            }
        )


#   View for API. Class include methods for search 
#       orders to params (number table, status)  
class OrderSearchAPI(APIView):
    def get(self, request):

        table_number = request.query_params.get('table_number')
        order_status = request.query_params.get('status')

        orders = Order.objects.all()
        #   Check data for emptiness. If not empty, filter is apply
        if table_number:
            orders = orders.filter(table_number=table_number)
        if order_status:
            orders = orders.filter(order_status=order_status)
        #   Apply the required data format
        serializer = OrderSerializer(orders, many=True)

        return Response(
            serializer.data, 
            status=status.HTTP_200_OK
        )


#   View for HTML page. Same as the API view (OrderSearchAPI)
class OrderSearchHTML(View):
    def get(self, request):

        table_number = request.GET.get('table_number')
        order_status = request.GET.get('status')


        orders = Order.objects.all()

        if table_number:
            orders = orders.filter(table_number=table_number)

        if order_status:
            orders = orders.filter(order_status=order_status)

        return render(
            request, 
            'orders/order_search.html', 
            {
                'orders': orders,
                'order_status_choices': OrderStatus.choices(),
            }
        )


#   View for API. Class include methods for 
#       count amount orders with status = 'paid'
class TotalAmountAPI(APIView):
    def get(self, request):
        #   Get orders, having status = 'paid' and count data in 'order_cost'
        #       If order with this status is not exist, return 0
        orders = Order.objects.all().filter(order_status='paid')
        result = orders.aggregate(total=Sum('order_cost'))['total'] or 0

        return Response(
            {'total': result},
            status=status.HTTP_200_OK
        )


#   View for HTML page. Same as the API view (TotalAmountAPI)
class TotalAmountHTML(View):
    def get(self, request):
        total_paid = Order.objects.filter(order_status='paid').aggregate(total=Sum('order_cost'))['total'] or 0
        return render(
            request, 
            'orders/order_total.html', 
            {
                'total': total_paid
            }
        )


class OrderChangeAPI(APIView):
    def post(self, request):
        #   Get value from request
        order_id = request.data.get('order_id')
        order = get_object_or_404(Order, pk=order_id)
        product_name = request.data.get('product_name')
        product_price = request.data.get('product_price')

        if not product_name or not product_price:
            return Response(
                {"error": "Both 'product_name' and 'product_price' are required."},
                status=status.HTTP_400_BAD_REQUEST,
            )
        #   Check fromat input price
        try:
            product_price = float(product_price)
        except ValueError:
            return Response(
                {"error": "'product_price' must be a valid number."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        #   Check order exists in DB
        if OrderDetail.objects.filter(order=order, product_name=product_name).exists():
            return Response(
                {"error": f"The product '{product_name}' already exists in this order."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        #   Create new record(order_id, name, price)
        detail = OrderDetail.objects.create(
            order=order,
            product_name=product_name,
            product_price=product_price,
        )

        #   Update finally order's cost
        order.order_cost = order.detail_order.aggregate(total=Sum('product_price'))['total'] or 0
        order.save()

        return Response(
            {
                "message": "Product added successfully.",
                "detail": 
                {
                    "id": detail.id,
                    "product_name": detail.product_name,
                    "product_price": detail.product_price,
                },
            },
            status=status.HTTP_201_CREATED,
        )
    
    #   Delete order's products
    def delete(self, request, order_id):
        order = get_object_or_404(Order, pk=order_id)
        product_name = request.data.get('product_name') or request.query_params.get('product_name')
        product_name = product_name.strip('"')

        if not product_name:
            return Response(
                {"error": "'product_name' is required for deletion."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        try:
            detail = OrderDetail.objects.get(product_name=product_name, order=order)
        except OrderDetail.DoesNotExist:
            return Response(
                {"error": f"Product {product_name} does not exist in this order."},
                status=status.HTTP_404_NOT_FOUND,
            )

        #   Delete product
        detail.delete()

        #   Update finally cost
        order.order_cost = order.detail_order.aggregate(total=Sum('product_price'))['total'] or 0
        order.save()

        return Response(
            {"message": f"Product {product_name} was successfully deleted."},
            status=status.HTTP_204_NO_CONTENT,
        )


#   View for HTML page. Same as the API view (OrderChangeAPI)
class OrderChangeHTML(View):
    def get(self, request):
        order_id = request.GET.get('order_id')

        if not order_id:
            return render(request, 'orders/order_change.html', {
                'order': None,
                'error': None,
            })

        #   Get order by ID
        try:
            order = Order.objects.get(pk=order_id)
        except Order.DoesNotExist:
            #   If not exists, get mistake
            return render(request, 'orders/order_change.html', {
                'order': None,
                'error': f"Order with ID {order_id} does not exist.",
            })
        order_details = order.detail_order.all()

        #   Get order
        return render(request, 'orders/order_change.html', {
            'order': order,
            'order_details': order_details,
        })

    def post(self, request):
        order_id = product_name = request.POST.get('order_id')
        try:
            order = Order.objects.get(pk=order_id)
        except Order.DoesNotExist:
            return render(request, 'orders/order_change.html', {
                'order': None,
                'error': f"Order with ID {order_id} does not exist.",
            })
        #   Check select action 
        action = request.POST.get('action')

        if action == 'add':
            product_name = request.POST.get('product_name')
            product_price = request.POST.get('product_price')

            if not product_name or not product_price:
                return render(request, 'orders/order_change.html', {
                    'order': order,
                    'order_details': order.detail_order.all(),
                    'error': 'Both product name and price are required for adding a product.',
                })

            try:
                product_price = float(product_price)
            except ValueError:
                return render(request, 'orders/order_change.html', {
                    'order': order,
                    'order_details': order.detail_order.all(),
                    'error': 'Invalid price format.',
                })

            if OrderDetail.objects.filter(order=order, product_name=product_name).exists():
                return render(request, 'orders/order_change.html', {
                    'order': order,
                    'order_details': order.detail_order.all(),
                    'error': f"The product '{product_name}' already exists in this order.",
                })

            OrderDetail.objects.create(
                order=order,
                product_name=product_name,
                product_price=product_price
            )

        elif action == 'remove':
            detail_id = request.POST.get('detail_id')
            try:
                detail = OrderDetail.objects.get(pk=detail_id, order=order)
                detail.delete()
            except OrderDetail.DoesNotExist:
                return render(request, 'orders/order_change.html', {
                    'order': order,
                    'order_details': order.detail_order.all(),
                    'error': f"Product with ID {detail_id} does not exist.",
                })

        total_cost = order.detail_order.aggregate(total=Sum('product_price'))['total'] or 0
        order.order_cost = total_cost
        order.save()

        return redirect(f'/orders/change/?order_id={order.id}')


#   View for API. Class include methods for get API functionality
class APIRoot(APIView):
    def get(self, request):
        return Response({
            "order-list-create": request.build_absolute_uri(reverse('api:api_order_list_create')),
            "order-change-status": 
            {
                "url": request.build_absolute_uri(reverse('api:api_order_change_status')),
                "body_example": 
                {
                    "order_id": 1,
                    "status": "paid"
                }
            },
            "order-delete": 
            {
                "template": "/api/orders/{id}/delete/",
                "example": request.build_absolute_uri(reverse('api:api_order_delete', kwargs={'order_id': 1}))
            },
            "order-search": {
                "url": request.build_absolute_uri(reverse('api:api_order_search')),
                "query_parameters": 
                {
                    "table_number": "int (optional)",
                    "status": "string (optional)"
                },
                "example": request.build_absolute_uri(
                    reverse('api:api_order_search') + "?table_number=5&status=paid"
                )
            },
            "order-total": 
            {
                "url": request.build_absolute_uri(reverse('api:api_order_total'))
            },
            "order-change": {
                "url": request.build_absolute_uri(reverse('api:api_order_change', kwargs={'order_id': 1})),
                "examples": {
                    "POST": {
                        "url": request.build_absolute_uri(reverse('api:api_order_change', kwargs={'order_id': 1})),
                        "body": {
                            "product_name": "Burger",
                            "product_price": 12.99
                        }
                    },
                    "DELETE": {
                        "url": request.build_absolute_uri(reverse('api:api_order_change', kwargs={'order_id': 1})),
                        "body": {
                            "detail_id": 2
                        }
                    }
                }
            }
        })


#   View for HTML page. Class include methods for get HTML pages
class APIRootHTML(View):
    def get(self, request):
        return render(
            request, 
            'orders/api_root.html', 
            {
                "order_get_add": reverse('html:html_order_list'),
                "order_delete": reverse('html:html_order_delete'),
                "order_change_status": reverse('html:html_order_change_status'),
                "order_search": reverse('html:html_order_search'),
                "order_total": reverse('html:html_order_total'),
                "order_change": reverse('html:html_order_change')
            }
        )
