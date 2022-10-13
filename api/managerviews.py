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


@api_view(['POST'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def Register_waiters(request):
    try:
        username = request.data['username']
        password = request.data['password']
        types = request.data['type']
        if int(types) == 1:
            users = User.objects.create_user(username=username, password=password,type=types,)
            token = Token.objects.create(user=users)
            data = {
                'username': username,
                'user_id': users.id,
                'token': token.key,
            }
            return Response(data)
        elif int(types) == 2:
            users = User.objects.create_user(username=username, password=password, type=types, )
            token = Token.objects.create(user=users)
            data = {
                'username': username,
                'user_id': users.id,
                'token': token.key,
            }
            return Response(data)
        else:
            return Response({'message':"you can only add a waiter or a cashier"})
    except Exception as err:
        return Response({'error': f'{err}'})

@api_view(['POST'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def login_waiters(request):
    user = request.user
    if user.type == 4:
        try:
            username = request.data['username']
            password = request.data['password']
            try:
                usrs = User.objects.get(username=username)
                user = authenticate(username=username, password=password)
                if user is not None:
                    status = 200
                    token, created = Token.objects.get_or_create(user=user)
                    data = {
                        'status': status,
                        'username': username,
                        'user_id': usrs.id,
                        'token': token.key,
                    }
                else:
                    status = 403
                    message = 'Username yoki parol xato!'
                    data = {
                        'status': status,
                        'message': message,
                    }
            except User.DoesNotExist:
                status = 404
                message = 'Bunday foydalanuvchi mavjud emas!'
                data = {
                    'status': status,
                    'message': message,
                }
            return Response(data)
        except Exception as er:
            return Response({"error": f'{er}'})
    else:
        return Response("You can't add Waiter because you are not Manager")


@api_view(['GET'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def all_waiters(request):
    user = request.user
    if user.type == 4:
        users = User.objects.filter(type=1)
        waiters = []
        for i in users:
            data = {
                "name": i.username,
                "id": i.id
            }
            waiters.append(data)
        return Response(waiters)


@api_view(['GET'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def all_cashiers(request):
    user = request.user
    if user.type == 4:
        users = User.objects.filter(type=2)
        cashiers = []
        for i in users:
            data = {
                "name": i.username,
                "id": i.id
            }
            cashiers.append(data)
        return Response(cashiers)

@api_view(['POST'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def delete_workers(request,):
    user = request.user
    if user.type == 4:
        ids = request.POST.get('name')
        users = User.objects.get(username=ids)
        if users.type == 1:
            User.objects.get(username=ids).delete()
            return Response({"message": "waiter deleted"})
        elif users.type == 2:
            User.objects.get(username=ids).delete()
            return Response({"message": "cashier deleted"})
        else:
            return Response({"message": "you can only delete cashier or waiter"})


@api_view(['POST'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def statistic_day(request):
    user = request.user
    if user.type == 4:

        day = request.POST.get("day")
        query = Payment.objects.filter(date__day=day)
        total = 0
        foods = []
        orders = []
        for i in query:
            total += i.money
            orders.append(i.order)
            for x in i.order.order.all():
                foods.append(x.food)
        data = {
            "total": total,
            "orders": len(orders),
            "selled foods": FoodSerializer(foods, many=True).data,

        }
        return Response(data)


@api_view(['POST'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def statistic_month(request):
    user = request.user
    if user.type == 4:
        month = request.POST.get("month")
        query = Payment.objects.filter(date__month=month)
        total = 0
        foods = []
        orders = []
        for i in query:
            total += i.money
            orders.append(i.order)
            for x in i.order.order.all():
                foods.append(x.food)
        data = {
            "total": total,
            "orders": len(orders),
            "selled foods": FoodSerializer(foods,  many=True).data,

        }
        return Response(data)


@api_view(['POST'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def statistic_year(request):
    user = request.user
    if user.type == 4:
        year = request.POST.get("year")
        query = Payment.objects.filter(date__year=year)
        total = 0
        foods = []
        orders = []
        for i in query:
            total += i.money
            orders.append(i.order)
            for x in i.order.order.all():
                foods.append(x.food)
        data = {
            "total": total,
            "orders": len(orders),
            "selled foods": FoodSerializer(foods, many=True).data,

        }
        return Response(data)


@api_view(['POST'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def AddProduct(request):
    user = request.user
    name = request.POST.get('name')
    quantity = request.POST.get('quantity')
    price = request.POST.get('price')
    type = request.POST.get('type')
    if user.type == 4:
        cash = Cash.objects.get(type=type)
        if cash.money <= int(price):
            product = Product.objects.create(name=name, quantity=quantity, price=price)
            Quitmoney.objects.create(product_id=product.id, price=price)

            cash.money = cash.money - int(price)
            cash.save()
            data = {
                'cash': CashSerializer(cash).data,

            }
            return Response(data)
        else:
            cash = Cash.objects.get(type=2)
            card = Cash.objects.get(type=1)
            data = {
                'habar': "Sizning hisobizda puliz yoq",
                'cash': CashSerializer(cash).data,
                'card': CashSerializer(card).data
            }
            return Response(data)
    else:
        return Response('Siz managermassiz')






@api_view(['GET'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def Spentmoney(request):
    user = request.user
    if user.type == 4 or user.type==3:
        data = {
            'QuitPrice': QuitmoneySerializer(Quitmoney.objects.all(), many=True).data,
            'QuitMoney': QuitpriceSerializer(Quitprice.objects.all(), many=True).data,
        }
        return Response(data)
    else:
        return Response({"message": "Siz korolmaysiz Chunki Director yoki Managermassiz okey"})






