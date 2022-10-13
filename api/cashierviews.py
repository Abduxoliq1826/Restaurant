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



# cashier
# get all
class GetAll(APIView):
    authentication_classes = [authentication.TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, pk):
        user = request.user
        if user.type == 2:
            product = []
            price = 0
            order = Order.objects.get(id=pk)
            for i in order.order.all():
                hello = {
                    'name': i.food.name,
                    'image': i.food.image.url,
                    'bio': i.food.description,
                    'price': i.food.price,
                    'quantity': i.quantity,
                }
                product.append(hello)
                price += i.food.price * i.quantity
            data = {
                'price': price,
                'product': product,
            }
            return Response(data)
        else:
            return Response(status=status.HTTP_400_BAD_REQUEST)


# cashier
# close table
@api_view(['POST'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def CloseOrder(request, pk):
    user = request.user
    type = request.POST.get('payment')
    if user.type == 2:
        price = 0
        order = Order.objects.get(id=pk)
        for i in order.order.all():
            price += i.food.price * i.quantity

        Payment.objects.create(money=price)
        cash = Cash.objects.get(type=int(type))
        cash.money += price
        cash.save()
        order.table.busyness = 1
        order.table.save()
        order.is_active = False
        order.save()

        return Response('ok')
    else:
        return Response("You can't close Order because you aren't cashier")

