import datetime
import json

from .models import *
from .forms import *

from django.contrib.auth.views import LoginView
from django.http import HttpResponse, JsonResponse, HttpResponseNotFound
from django.shortcuts import render, redirect

from django.contrib.auth.models import auth
from django.contrib.auth import authenticate

from django.urls import reverse_lazy

from django.views.generic import *
from django.core.exceptions import ObjectDoesNotExist


def home(request):
    latest_article = Article.objects.latest('published_date')
    return render(request, 'home.html', {'latest_article': latest_article})


def about_company(request):
    company_info = CompanyInfo.objects.first()
    return render(request, 'about_company.html', {'company_info': company_info})


def news(request):
    all_news = Article.objects.all()
    return render(request, 'news.html', {'all_news': all_news})


def terms(request):
    all_terms = Term.objects.all()
    return render(request, 'terms.html', {'all_terms': all_terms})


def contacts(request):
    all_contacts = Contact.objects.all()
    return render(request, 'contacts.html', {'all_contacts': all_contacts})


def vacancies(request):
    all_vacancies = Vacancy.objects.all()
    return render(request, 'vacancies.html', {'all_vacancies': all_vacancies})


def privacy_policy(request):
    return render(request, 'privacy_policy.html')


class ReviewListView(ListView):
    model = Review
    queryset = Review.objects.all()
    template_name = 'reviews.html'


class ReviewCreateView(View):
    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated and request.user.status == 'customer':
            form = ReviewForm(request.GET)
            return render(request, 'add_review.html', {'form': form})
        return redirect('login')

    def post(self, request, *args, **kwargs):
        if request.user.is_authenticated and request.user.status == 'customer':
            form = ReviewForm(request.POST)
            if form.is_valid():
                form.save()
                return redirect('reviews')
        return redirect('login')


class UserRegistrationView(CreateView):
    def post(self, request, *args, **kwargs):
        form = RegistrationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.save()
            return redirect('login')
        else:
            return render(request, 'register.html', {'form': form})

    def get(self, request, *args, **kwargs):
        form = RegistrationForm()
        return render(request, 'register.html', {'form': form})


class UserAuthorizationView(LoginView):
    redirect_authenticated_user = True
    template_name = 'login.html'

    def get_success_url(self):
        return reverse_lazy('home')


class UserLogoutView(View):
    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            auth.logout(request)
        return redirect('home')


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
                'amount': product.amount,
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
        if Product.objects.filter(pk=self.kwargs.get("pk")).exists():
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
        return HttpResponseNotFound('page not found')


class OrderCreateView(View):
    def get(self, request, pk, *args, **kwargs):
        if request.user.is_authenticated and request.user.status == "customer" and\
                Product.objects.filter(pk=pk).exists():
            product = Product.objects.get(pk=pk)
            form = OrderForm()
            context = {
                'product': product,
                'form': form,
            }
            return render(request, 'order_form.html', context)
        return HttpResponseNotFound('page not found')

    def post(self, request, pk, *args, **kwargs):
        if request.user.is_authenticated and request.user.status == "customer" and \
                Product.objects.filter(pk=pk).exists():
            product = Product.objects.get(pk=pk)
            form = OrderForm(request.POST)

            if form.is_valid():
                amount = form.cleaned_data['amount']

                if product.amount - amount >= 0:
                    order = Order.objects.create(user=request.user, product=product, amount=amount,
                                                 price=amount * product.price)

                    order_data = {
                        "user": order.user.username,
                        "number": order.number,
                        "product_id": order.product.id,
                        "price": order.price,
                        "promo": order.promo_code,
                        "amount": order.amount,
                        "date": order.date,
                        "is_active": order.is_active,
                    }

                    product.amount -= amount
                    product.save()
                    return JsonResponse(order_data, safe=False)
                return HttpResponse('There are not enough products in stock to place an order')
        elif request.user.is_authenticated and request.user.status == "employee":
            return HttpResponseNotFound("Page not found")
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
                        "price": order.price,
                        "promo": order.promo_code,
                        "amount": order.amount,
                        "date": order.date,
                        "is_active": order.is_active,
                    })
                return JsonResponse(orders_data, safe=False)
            except ObjectDoesNotExist:
                return HttpResponseNotFound("Page not found")
        return HttpResponseNotFound("Page not found")


class OrderDeleteDetailView(View):
    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated and request.user.status == "employee" \
                and Order.objects.filter(pk=self.kwargs.get("pk")).exists():
            pk = self.kwargs.get("pk")
            order = Order.objects.get(pk=pk)

            order_data = {
                "user": order.user.username,
                "number": order.number,
                "product_id": order.product.id,
                "price": order.price,
                "promo": order.promo_code,
                "amount": order.amount,
                "date": order.date,
                "is_active": order.is_active,
            }
            return JsonResponse(order_data, safe=False)
        elif request.user.is_authenticated and request.user.status == "customer" \
                and Order.objects.filter(pk=self.kwargs.get("pk"), user_id=request.user.id).exists():
            pk = self.kwargs.get("pk")
            order = Order.objects.get(pk=pk, user_id=request.user.id)
            form = OrderDeleteForm()
            return render(request, 'order_detail.html', {'form': form, 'order': order})
        return HttpResponseNotFound("Page not found")

    def post(self, request, *args, **kwargs):
        if request.user.is_authenticated and request.user.status == "customer" \
                and Order.objects.filter(pk=self.kwargs.get("pk")).exists():
            form = OrderDeleteForm(request.POST)

            if form.is_valid():
                order_id = self.kwargs.get("pk")
                order = Order.objects.filter(pk=order_id, user=request.user).first()

                if order:
                    order_data = {
                        "user": order.user.username,
                        "number": order.number,
                        "product_id": order.product.id,
                        "price": order.price,
                        "promo": order.promo_code,
                        "amount": order.amount,
                        "date": order.date,
                        "is_active": order.is_active,
                    }

                    order.product.amount += order.amount
                    order.product.save()
                    order.delete()
                    return JsonResponse(order_data, safe=False)
        return HttpResponseNotFound("Page not found")


class UserOrderListView(View):
    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated and request.user.status == "employee" or \
                request.user.is_authenticated and request.user.status == "customer" and \
                self.kwargs.get("pk") == request.user.id:
            pk = self.kwargs.get("pk")

            orders = Order.objects.filter(user_id=pk)
            if orders:
                orders_data = []
                for order in orders:
                    orders_data.append({
                        "number": order.number,
                        "product_id": order.product.id,
                        "price": order.price,
                        "promo": order.promo_code,
                        "amount": order.amount,
                        "date": order.date,
                        "is_active": order.is_active,
                    })
                return JsonResponse(orders_data, safe=False)
            else:
                return HttpResponse("There are no orders")
        return HttpResponseNotFound("Page not found")


class PurchaseCreateView(View):
    def get(self, request, pk, *args, **kwargs):
        if request.user.is_authenticated and request.user.status == "customer" \
                and Order.objects.filter(pk=self.kwargs.get("pk"), user=request.user, is_active=True).exists():
            order = Order.objects.get(pk=pk)
            form = PurchaseCreateForm()
            context = {
                'order': order,
                'form': form,
            }
            return render(request, 'purchase_form.html', context)
        return HttpResponseNotFound('page not found')

    def post(self, request, *args, **kwargs):
        if request.user.is_authenticated and request.user.status == "customer" \
                and Order.objects.filter(pk=self.kwargs.get("pk"), user=request.user, is_active=True).exists():
            form = PurchaseCreateForm(request.POST)

            if form.is_valid():
                pk = self.kwargs.get("pk")
                order = Order.objects.get(pk=pk, user=request.user, is_active=True)

                delivery_datetime = datetime.datetime.now() + datetime.timedelta(days=1)
                delivery_datetime = delivery_datetime.replace(hour=17, minute=0, second=0, microsecond=0)

                promo_code = form.cleaned_data["promo_code"]
                promo = Promo.objects.filter(code=promo_code).first()

                if promo:
                    order.apply_promo(promo)

                purchase = Purchase.objects.create(
                    user=request.user,
                    order=order,
                    town=form.cleaned_data["town"],
                    delivery_date=delivery_datetime
                )

                order.is_active = False
                order.save()

                purchase_data = {
                    "order_id": order.number,
                    "user_id": request.user.id,
                    "town": form.cleaned_data["town"],
                    "purchase_date": purchase.purchase_date,
                    "delivery_date": purchase.delivery_date,
                }
                return JsonResponse(purchase_data, safe=False)
        return HttpResponseNotFound("Page not found")


class PurchaseListView(View):
    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated and request.user.status == "employee":
            try:
                purchases = Purchase.objects.all()

                purchases_data = []
                for purchase in purchases:
                    purchases_data.append({
                        "order_id": purchase.order.number,
                        "user_id": purchase.order.user.id,
                        "username": purchase.order.user.username,
                        "town": purchase.town,
                        "purchase_date": purchase.purchase_date,
                        "delivery_date": purchase.delivery_date,
                    })
                return JsonResponse(purchases_data, safe=False)
            except ObjectDoesNotExist:
                return HttpResponseNotFound("Page not found")
        return HttpResponseNotFound("Page not found")


class PurchaseDetailView(View):

    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated and request.user.status == "employee" \
                and Purchase.objects.filter(pk=self.kwargs.get("pk")).exists():
            pk = self.kwargs.get("pk")
            purchase = Purchase.objects.get(pk=pk)

            purchase_data = {
                "order_id": purchase.order.number,
                "user_id": purchase.order.user.id,
                "username": purchase.order.user.username,
                "town": purchase.town,
                "purchase_date": purchase.purchase_date,
                "delivery_date": purchase.delivery_date,
            }
            return JsonResponse(purchase_data, safe=False)
        elif request.user.is_authenticated and request.user.status == "customer" \
                and Purchase.objects.filter(pk=self.kwargs.get("pk"), user_id=request.user.id).exists():
            pk = self.kwargs.get("pk")
            purchase = Purchase.objects.get(pk=pk, user_id=request.user.id)

            purchase_data = {
                "order_id": purchase.order.number,
                "user_id": purchase.order.user.id,
                "username": purchase.order.user.username,
                "town": purchase.town,
                "purchase_date": purchase.purchase_date,
                "delivery_date": purchase.delivery_date,
            }
            return JsonResponse(purchase_data, safe=False)
        return HttpResponseNotFound("Page not found")


class PromoListView(View):
    def get(self, request, *args, **kwargs):
        promos = Promo.objects.all()
        promos_data = []

        for promo in promos:
            promos_data.append({
                "code": promo.code,
                "discount": promo.discount,
            })
        return JsonResponse(promos_data, safe=False)
