from django.shortcuts import render
from .models import *
from rest_framework import authentication, permissions
from rest_framework.decorators import api_view, permission_classes, authentication_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from .serializers import *
from rest_framework.views import APIView
from rest_framework.authentication import TokenAuthentication
from rest_framework.authtoken.models import Token
from django.contrib.auth import authenticate
from rest_framework import status


# waiter
# get menu
class GetMenyu(APIView):
    authentication_classes = [authentication.TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        user = request.user
        if user.type == 1:
            product = Food.objects.filter(available=True)
            food = []
            for i in product:

                data = {

                   'name': i.name,
                   'image': i.image.url,
                   'bio': i.description,
                   'price': i.price
                }
                food.append(data)
                return Response(food)


@api_view(['POST'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def OrderItemcreate(request):
    user = request.user
    if user.type == 1:
        food = request.POST.get('food')
        quantity = request.POST.get('quantity')
        order = OrderItem.objects.create(food_id=food, quantity=quantity)
        return Response(OrderItemSerializer(order).data)



# waiter
# create order
@api_view(['POST'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def Ordercreated(request):
    user = request.user
    item = request.POST.getlist('item')
    table = request.POST.get('table')
    if Table.objects.get(id=table).busyness == 1:
        order = Order.objects.create(table_id=int(table), user=user)
        for i in item:
            order.order.add(OrderItem.objects.get(id=int(i)))
        tables = Table.objects.get(id=table)
        tables.busyness = 2
        tables.save()
        return Response(OrderSerializer(order).data)
    else:
        return Response('this table busy')


# waiter
# update
@api_view(['POST'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def Update(request, pk):
    user = request.user
    table = request.POST.get('table')
    orderitem = request.POST.getlist('order')
    order = Order.objects.get(id=pk)
    if user.type == 1:
        order.table_id = table
        for i in orderitem:
            order.order_id = int(i)
        order.save()
        return Response(OrderSerializer(order).data)

@api_view(['GET'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def Myaccaunt(request):
    user = request.user
    if user.type == 1:
        price = 0
        order = Order.objects.filter(user=user)
        for i in order:
            price += 5000
        data = {
            'salary': price,
            'order': OrderSerializer(order, many=True).data,
        }
        return Response(data)
    else:
        return Response("You can't waiter")



@api_view(['POST'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def Salary(request):
    user = request.user
    if user.type == 1:
        order = Order.objects.filter(user=user)
        count = order.count()

        salary = count * 5000

        data = {
            'salary': "Bugungi kunlik oylig'ingiz  ",
            'pul': salary,
        }
        return Response()
