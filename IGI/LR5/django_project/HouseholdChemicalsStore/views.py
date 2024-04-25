from django.shortcuts import render
from .models import *
from django.views.decorators.csrf import csrf_exempt
import json
from django.http import HttpResponse

from django.contrib.auth.models import auth
from django.contrib.auth import authenticate

@csrf_exempt
def register(request):
    body_unicode = request.body.decode('utf-8')
    body = json.loads(body_unicode)
    User.objects.create_user(username=body["username"],
                             password=body["password"],
                             email=body["email"],
                             status=body["status"],
                             )
    return HttpResponse('user successfully registered!')

@csrf_exempt
def my_login(request):
    body_unicode = request.body.decode('utf-8')
    body = json.loads(body_unicode)
    user = authenticate(request, username=body["username"], password=body["password"])

    if user is not None:
        auth.login(request, user)

        return HttpResponse('login successfully!')

    return HttpResponse('login unsuccessfully!')

def get_products(request):
    products = Product.objects.all()
    products_data = []
    for product in products:
        products_data.append({
            'name': product.name,
            'producer_id': product.producer,
        })
    return HttpResponse(products_data)

def get_products_by_producer(request, producer_name):
    producer = Producer.objects.get(name=producer_name)
    products = Product.objects.filter(producer_id=producer.id)
    products_data = []
    for product in products:
        products_data.append({
            'name': product.name,
            'producer_id': producer.id,
        })
    return HttpResponse(products_data)
