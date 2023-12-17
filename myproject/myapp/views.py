from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework import viewsets, status
from rest_framework.response import Response
from .models import Person, OrderHeader, OrderItem, Product, OrderPart
from .serializers import PersonSerializer, OrderSerializer
from django.shortcuts import get_object_or_404
from django.http import HttpResponse

# views.py


def home(request):
    return HttpResponse("Welcome to my project!")


class PersonViewSet(viewsets.ModelViewSet):
    queryset = Person.objects.all()
    serializer_class = PersonSerializer


class OrderViewSet(viewsets.ModelViewSet):
    queryset = OrderHeader.objects.all()
    serializer_class = OrderSerializer


#endpoints
@api_view(["POST"])
def create_order(request):
    data = request.data.copy()  # copy the request data

    # Set default values if not provided in the request
    data.setdefault("currencyUomId", "USD")
    data.setdefault("statusId", "OrderPlaced")

    serializer = OrderSerializer(data=data)

    if serializer.is_valid():
        order = serializer.save()
        return Response({"ORDER_ID": order.orderId}, status=status.HTTP_201_CREATED)

    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(["POST"])
def add_order_items(request):
    print("inside the method")
    try:
        # Extract data from the request
        print(request.data.get("ORDER_ID"))
        order_id = request.data.get("ORDER_ID")
        part_name = request.data.get("PART_NAME")
        facility_id = request.data.get("FACILITY_ID")
        shipment_method_enum_id = request.data.get(
            "SHIPMENT_METHOD_ENUM_ID", "ShMthGround"
        )
        customer_party_id = request.data.get("CUSTOMER_PARTY_ID")
        item_details = request.data.get("ITEM_DETAILS")

        # Get the existing order
        order = OrderHeader.objects.get(ORDER_ID=order_id)
        order_part = OrderPart.objects.get(ORDER_ID=order_id)

        print('order part', order_part.__dict__)

        # Iterate through item details and create order items
        for item_detail in item_details:
            product_id = item_detail["PRODUCT_ID"]
            item_description = item_detail["ITEM_DESCRIPTION"]
            quantity = item_detail["QUANTITY"]
            unit_amount = item_detail["UNIT_AMOUNT"]

            product = Product.objects.get(PRODUCT_ID=product_id)
            order_item = OrderItem.objects.create(
                ORDER_ID=order,
                PRODUCT_ID=product,
                ITEM_DESCRIPTION=item_description,
                QUANTITY=quantity,
                UNIT_AMOUNT=unit_amount
            )

        return Response(
            {
                "ORDER_ID": order.ORDER_ID,
                "ORDER_PART_SEQ_ID": order_part.ORDER_PART_SEQ_ID,
            },
            status=status.HTTP_201_CREATED,
        )

    except OrderHeader.DoesNotExist:
        return Response({"error": "Order not found."}, status=status.HTTP_404_NOT_FOUND)

    except Exception as e:
        return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)


@api_view(["GET"])
def get_orders(request):
    orders = OrderHeader.objects.all()
    serializer = OrderSerializer(orders, many=True)
    response_data = {"orders": serializer.data}
    return Response(response_data)


@api_view(["GET"])
def get_order(request, order_id):
    order = get_object_or_404(OrderHeader, ORDER_ID=order_id)
    serializer = OrderSerializer(order)
    return Response(serializer.data)


@api_view(["PUT"])
def update_order(request, order_id):
    order_id = request.data.get("ORDER_ID")
    print(request.data)
    order = get_object_or_404(OrderHeader, ORDER_ID=order_id)
    serializer = OrderSerializer(instance=order, data=request.data, partial=True)

    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data)
    else:
        return Response(serializer.errors, status=400)
