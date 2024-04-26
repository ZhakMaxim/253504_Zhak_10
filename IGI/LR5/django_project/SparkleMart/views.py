from .models import *
from django.views.decorators.csrf import csrf_exempt
import json
from django.http import HttpResponse, JsonResponse, HttpResponseRedirect, HttpResponseNotFound

from django.contrib.auth.models import auth
from django.contrib.auth import authenticate

from django.views.generic import *
from django.core.exceptions import ObjectDoesNotExist

class UserRegistrationView(View):
    @csrf_exempt
    def post(self, request):
        body_unicode = request.body.decode('utf-8')
        body = json.loads(body_unicode)

        user = User.objects.create_user(username=body["username"],
                                        password=body["password"],
                                        email=body["email"],
                                        phone_number=body["phone_number"],
                                        status=body["status"],
                                        )
        if user:
            user_data = {
                "username": body["username"],
                "password": body["password"],
                "email": body["email"],
                "phone_number": body["phone_number"],
                "status": body["status"],
            }
            return JsonResponse(user_data, safe=False)
        return HttpResponse('error while creating user!')


class UserAuthorizationView(View):
    @csrf_exempt
    def post(self, request):
        body_unicode = request.body.decode('utf-8')
        body = json.loads(body_unicode)
        user = authenticate(request, username=body["username"], password=body["password"])

        if user is not None:
            auth.login(request, user)

            user_data = {
                "username": body["username"],
                "password": body["password"],
                "email": body["email"],
                "phone_number": body["phone_number"],
                "status": body["status"],
            }

        return HttpResponse('login unsuccessfully!')

class UserLogoutView(View):
    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            auth.logout(request)
        return HttpResponseRedirect('/products')

class UserListView(View):
    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated and request.user.status == "employee":
            users = User.objects.filter(status="customer")
            users_data = []
            for user in users:
                users_data.append({
                    "id": user.id,
                    "username": user.username,
                    "phone_number": user.phone_number,
                    "email": user.email,
                })
            return JsonResponse(users_data, safe=False)
        return HttpResponseNotFound("Page not found")

class UserDetailView(View):
    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated and request.user.status == "employee":
            pk = self.kwargs.get("pk")
            user = User.objects.get(pk=pk)
            if user.status != "employee":
                user_data = {
                    "id": user.id,
                    "username": user.username,
                    "phone_number": user.phone_number,
                    "email": user.email,
                    }
                return JsonResponse(user_data, safe=False)
        return HttpResponseNotFound("Page not found")

class ProductListView(ListView):
    model = Product
    queryset = Product.objects.all()

    def get(self, request, *args, **kwargs):
        min_price = request.GET.get('min_price')
        max_price = request.GET.get('max_price')
        category_id = request.GET.get('category_id')
        producer_id = request.GET.get('producer_id')

        products = self.filter_products(min_price, max_price, producer_id, category_id)

        products_data = []
        for product in products:
            categories = list(product.category.all().values_list('name', flat=True))
            products_data.append({
                'id': product.id,
                'name': product.name,
                'price': product.price,
                'category': categories,
                'producer_id': product.producer.id,
            })
        return JsonResponse(products_data, safe=False)

    @staticmethod
    def filter_products(min_price=None, max_price=None, producer=None, category=None):
        products = Product.objects.all()

        filtered_products = None

        if category:
            products = products.filter(category=category)
        if producer:
            products = products.filter(producer=producer)

        if min_price is not None and max_price is not None:
            filtered_products = products.filter(price__gte=min_price, price__lte=max_price)
        elif min_price is not None:
            filtered_products = products.filter(price__gte=min_price)
        elif max_price is not None:
            filtered_products = products.filter(price__lte=max_price)

        if filtered_products is not None:
            return filtered_products
        return products


class ProductDetailView(DetailView):
    model = Product

    def get(self, request, *args, **kwargs):
        product = self.get_object()
        categories = list(product.category.all().values_list('name', flat=True))

        product_data = {
            'id': product.id,
            'name': product.name,
            'price': product.price,
            'category': categories,
            'producer_id': product.producer.id,
        }
        return JsonResponse(product_data)


class OrderCreateView(View):
    def get(self, request, pk, *args, **kwargs):
        if request.user.is_authenticated and request.user.status == "customer":
            product = Product.objects.get(pk=pk)
            body_unicode = request.body.decode('utf-8')
            body = json.loads(body_unicode)
            amount = body["amount"]
            order = Order.objects.create(user=request.user, product=product, amount=amount, price=amount*product.price)
            return HttpResponse('order successfully created!')
        else:
            return HttpResponse('please, login for making order!')


class OrderListView(View):
    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated and request.user.status == "employee":
            try:
                orders = Order.objects.all()
                orders_data = []
                for order in orders:
                    orders_data.append({
                        "user": order.user.username,
                        "number": order.number,
                        "product_id": order.product.id,
                        "date": order.date,
                    })
                return JsonResponse(orders_data, safe=False)
            except ObjectDoesNotExist:
                return HttpResponseNotFound("Page not found")
        return HttpResponseNotFound("Page not found")

class OrderDetailView(View):
    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated and request.user.status == "employee":
            try:
                pk = self.kwargs.get("pk")
                order = Order.objects.get(pk=pk)
                order_data = {
                    "user": order.user.username,
                    "number": order.number,
                    "product_id": order.product.id,
                    "amount": order.amount,
                    "date": order.date,
                    }
                return JsonResponse(order_data, safe=False)
            except ObjectDoesNotExist:
                return HttpResponseNotFound("Page not found")
        elif request.user.is_authenticated and request.user.status == "customer":
            try:
                pk = self.kwargs.get("pk")
                order = Order.objects.get(pk=pk, user_id=request.user.id)
                order_data = {
                    "user": order.user.username,
                    "number": order.number,
                    "product_id": order.product.id,
                    "amount": order.amount,
                    "date": order.date,
                }
                return JsonResponse(order_data, safe=False)
            except ObjectDoesNotExist:
                return HttpResponseNotFound("Page not found")


class UserOrderListView(View):
    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated and request.user.status == "employee" or\
            request.user.is_authenticated and request.user.status == "customer" and\
                self.kwargs.get("pk") == request.user.id:
            pk = self.kwargs.get("pk")
            orders = Order.objects.filter(user_id=pk)
            if orders:
                orders_data = []
                for order in orders:
                    orders_data.append({
                        "number": order.number,
                        "product_id": order.product.id,
                        "amount": order.amount,
                        "date": order.date,
                    })
                return JsonResponse(orders_data, safe=False)
            else:
                return HttpResponse("There are no orders")
        return HttpResponseNotFound("Page not found")