import datetime

from .models import *
from .forms import *

from django.contrib.auth.views import LoginView
from django.http import HttpResponse, JsonResponse, HttpResponseNotFound
from django.shortcuts import render, redirect

from django.utils import timezone

from django.contrib.auth.models import auth

from django.urls import reverse_lazy

from django.views.generic import *
from django.core.exceptions import ObjectDoesNotExist

import requests

import logging

logging.basicConfig(level=logging.INFO, filename='logs.log', filemode='a',
                    format='%(asctime)s %(levelname)s %(message)s')

def home(request):
    latest_article = Article.objects.latest('published_date')
    logging.info(f'latest article title: {latest_article.title}')
    return render(request, 'home.html', {'latest_article': latest_article})


def about_company(request):
    company_info = CompanyInfo.objects.first()
    logging.info(f'company info: {company_info.text}')
    return render(request, 'about_company.html', {'company_info': company_info})


def news(request):
    all_news = Article.objects.all()
    logging.info(f'news titles: {[new.title for new in all_news]}')
    return render(request, 'news.html', {'all_news': all_news})


def terms(request):
    all_terms = Term.objects.all()
    logging.info(f'terms questions: {[term.question for term in all_terms]}')
    return render(request, 'terms.html', {'all_terms': all_terms})


def contacts(request):
    all_contacts = Contact.objects.all()
    logging.info(f'contacts names: {[contact.name for contact in all_contacts]}')
    return render(request, 'contacts.html', {'all_contacts': all_contacts})


def vacancies(request):
    all_vacancies = Vacancy.objects.all()
    logging.info(f'vacancies titles: {[vacancy.name for vacancy in all_vacancies]}')
    return render(request, 'vacancies.html', {'all_vacancies': all_vacancies})


def privacy_policy(request):
    return render(request, 'privacy_policy.html')


def random_fact(request):
    url = 'https://favqs.com/api/qotd'
    fact = requests.get(url.format()).json()
    return JsonResponse(fact, safe=False)


def random_joke(request):
    url = 'https://official-joke-api.appspot.com/random_joke'
    joke = requests.get(url.format()).json()
    return JsonResponse(joke, safe=False)


def profile(request):
    if request.user.is_authenticated and request.user.status == 'customer':
        form = PhoneNumberChangeForm(request.POST or None, instance=request.user)
        if request.method == 'POST':
            if form.is_valid():
                form.save()
                return redirect('profile')
        return render(request, 'profile.html', {'form': form})
    logging.warning('profile view: page not found')
    return render(request, 'page_not_found.html', status=404)


class ReviewListView(ListView):
    model = Review
    queryset = Review.objects.all()
    template_name = 'reviews.html'


class ReviewCreateView(View):
    def get(self, request, **kwargs):
        if request.user.is_authenticated and request.user.status == 'customer' and not request.user.is_superuser:
            form = ReviewForm(request.GET)
            return render(request, 'add_review.html', {'form': form})
        return redirect('login')

    def post(self, request, *args, **kwargs):
        if request.user.is_authenticated and request.user.status == 'customer' and not request.user.is_superuser:
            form = ReviewForm(request.POST)
            if form.is_valid():
                form.save()
                logging.info('created Review object!')
                return redirect('reviews')
        return redirect('login')


class UserRegistrationView(CreateView):
    # def post(self, request, *args, **kwargs):
    #     form = RegistrationForm(request.POST)
    #     if form.is_valid():
    #         user = form.save(commit=False)
    #         user.save()
    #         return redirect('login')
    #     else:
    #         return render(request, 'register.html', {'form': form})
    #
    # def get(self, request, *args, **kwargs):
    #     form = RegistrationForm()
    #     return render(request, 'register.html', {'form': form})

    form_class = RegistrationForm
    template_name = 'register.html'
    success_url = '/login/'

    def form_valid(self, form):
        user = form.save(commit=False)
        user.save()
        logging.info('user successfully registered!')
        return super().form_valid(form)


class UserAuthorizationView(LoginView):
    redirect_authenticated_user = True
    template_name = 'login.html'

    def get_success_url(self):
        logging.info('user successfully authorised!')
        return reverse_lazy('home')


class UserLogoutView(View):
    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            auth.logout(request)
            logging.info('user successfully logout!')
        return redirect('home')


class UserListView(View):
    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated and request.user.status == "employee":
            users = User.objects.filter(status="customer", is_superuser=False)

            users_data = []
            for user in users:
                users_data.append({
                    "id": user.id,
                    "username": user.username,
                    "phone_number": user.phone_number,
                    "email": user.email,
                })
            return JsonResponse(users_data, safe=False)
        logging.warning('UserListView: page not found')
        return render(request, 'page_not_found.html', status=404)


class UserDetailView(View):
    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated and request.user.status == "employee" and \
                User.objects.filter(pk=self.kwargs.get("pk"), is_superuser=False):
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
            logging.warning('UserDetailView: page not found')
        return render(request, 'page_not_found.html', status=404)


class ProductListView(ListView):
    model = Product
    queryset = Product.objects.all()

    def get(self, request, *args, **kwargs):
        min_price = request.GET.get('min_price')
        max_price = request.GET.get('max_price')
        category_name = request.GET.get('cat_name')
        producer_name = request.GET.get('prod_name')

        products = self.filter_products(min_price, max_price, producer_name, category_name)

        products_data = []
        for product in products:
            categories = list(product.category.all().values_list('name', flat=True))

            products_data.append({
                'id': product.id,
                'name': product.name,
                'price': product.price,
                'amount': product.amount,
                'category': categories,
                'producer_name': producer_name,
                'producer_id': product.producer.id,
            })
        return JsonResponse(products_data, safe=False)

    @staticmethod
    def filter_products(min_price=None, max_price=None, prod_name=None, cat_name=None):
        products = Product.objects.all()

        filtered_products = None

        if cat_name:
            if Category.objects.filter(name=cat_name).exists():
                category = Category.objects.get(name=cat_name)
                products = products.filter(category=category)
        if prod_name:
            if Producer.objects.filter(name=prod_name).exists():
                producer = Producer.objects.get(name=prod_name)
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
                'producer_name': product.producer.name,
                'producer_id': product.producer.id,
            }
            return JsonResponse(product_data)
        logging.warning('ProductDetailView: page not found')
        return render(request, 'page_not_found.html', status=404)


class OrderCreateView(View):
    def get(self, request, pk, *args, **kwargs):
        if request.user.is_authenticated and request.user.status == "customer" and \
                Product.objects.filter(pk=pk).exists():
            product = Product.objects.get(pk=pk)
            form = OrderForm()
            context = {
                'product': product,
                'form': form,
            }
            return render(request, 'order_form.html', context)
        logging.warning('OrderCreateView: page not found')
        return render(request, 'page_not_found.html', status=404)

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
                        "date": timezone.localtime(order.date),
                        "is_active": order.is_active,
                    }

                    product.amount -= amount
                    product.save()
                    logging.info('created Order object')
                    return JsonResponse(order_data, safe=False)
                return HttpResponse('There are not enough products in stock to place an order')
        elif request.user.is_authenticated and request.user.status == "employee":
            logging.warning('OrderCreateView: page not found')
            return render(request, 'page_not_found.html', status=404)
        else:
            logging.warning('OrderCreateView: user is not authenticated')
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
                        "date": timezone.localtime(order.date),
                        "is_active": order.is_active,
                    })
                return JsonResponse(orders_data, safe=False)
            except ObjectDoesNotExist:
                logging.warning('OrderListView: page not found')
                return render(request, 'page_not_found.html', status=404)
        logging.warning('OrderListView: page not found')
        return render(request, 'page_not_found.html', status=404)


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
                "date": timezone.localtime(order.date),
                "is_active": order.is_active,
            }
            return JsonResponse(order_data, safe=False)
        elif request.user.is_authenticated and request.user.status == "customer" \
                and Order.objects.filter(pk=self.kwargs.get("pk"), user_id=request.user.id).exists():
            pk = self.kwargs.get("pk")
            order = Order.objects.get(pk=pk, user_id=request.user.id)
            form = OrderDeleteForm()
            return render(request, 'order_detail.html', {'form': form, 'order': order})
        logging.warning('OrderDeleteView: page not found')
        return render(request, 'page_not_found.html', status=404)

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
                        "date": timezone.localtime(order.date),
                        "is_active": order.is_active,
                    }

                    order.product.amount += order.amount
                    order.product.save()
                    order.delete()
                    logging.warning('deleted Order object')
                    return JsonResponse(order_data, safe=False)
        logging.warning('OrderDeleteView: page not found')
        return render(request, 'page_not_found.html', status=404)


class UserOrderListView(View):
    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated and request.user.status == "employee" or\
                request.user.is_authenticated and request.user.status == "customer" and\
                self.kwargs.get("pk") == str(request.user.pk) and not User.objects.filter(
                    pk=self.kwargs.get("pk")).first().is_superuser and not User.objects.filter(
                    pk=self.kwargs.get("pk")).first().status == 'employee':
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
                        "date": timezone.localtime(order.date),
                        "is_active": order.is_active,
                    })
                return JsonResponse(orders_data, safe=False)
            else:
                logging.warning('UserOrderListView: no orders')
                return HttpResponse("There are no orders")
        logging.warning('UserOrderListView: page not found')
        return render(request, 'page_not_found.html', status=404)


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
        logging.warning('PurchaseCreateView: page not found')
        return render(request, 'page_not_found.html', status=404)

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

                logging.info('created Purchase object')

                purchase_data = {
                    "order_id": order.number,
                    "user_id": request.user.id,
                    "town": form.cleaned_data["town"],
                    "purchase_date": timezone.localtime(purchase.purchase_date),
                    "delivery_date": purchase.delivery_date,
                }
                return JsonResponse(purchase_data, safe=False)
        logging.warning('PurchaseCreateView: page not found')
        return render(request, 'page_not_found.html', status=404)


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
                        "purchase_date": timezone.localtime(purchase.purchase_date),
                        "delivery_date": timezone.localtime(purchase.delivery_date),
                    })
                return JsonResponse(purchases_data, safe=False)
            except ObjectDoesNotExist:
                logging.warning('PurchaseListView: page not found')
                return render(request, 'page_not_found.html', status=404)
        logging.warning('purchaseListView: page not found')
        return render(request, 'page_not_found.html', status=404)


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
                "purchase_date": timezone.localtime(purchase.purchase_date),
                "delivery_date": timezone.localtime(purchase.delivery_date),
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
                "purchase_date": timezone.localtime(purchase.purchase_date),
                "delivery_date": timezone.localtime(purchase.delivery_date),
            }
            return JsonResponse(purchase_data, safe=False)
        logging.warning('PurchaseDetailView: page not found')
        return render(request, 'page_not_found.html', status=404)


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


class PickUpPointListView(View):
    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            pick_up_points = PickUpPoint.objects.all()
            if pick_up_points:
                pick_up_points_data = []
                for pick_up_point in pick_up_points:
                    pick_up_points_data.append({
                        'address': pick_up_point.address,
                    })
                return JsonResponse(pick_up_points_data, safe=False)
            logging.warning('PickUpPointsListView: no pick up points')
            return render(request, 'page_not_found.html', status=404)
        logging.warning('PickUpPointsListView: page not found')
        return render(request, 'page_not_found.html', status=404)
