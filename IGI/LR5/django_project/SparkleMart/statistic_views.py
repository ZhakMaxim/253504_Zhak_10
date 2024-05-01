import base64
import io
from datetime import datetime
from urllib import parse

import numpy as np

import matplotlib
from django.db.models import Sum

from .models import *
from matplotlib import pyplot as plt
from django.shortcuts import render

from django.db.models.functions import TruncMonth

from statistics import median

from django.db.models import Count

def most_popular_category():
    category_purchases = Order.objects.values('product__category__name').annotate(
        purchase_count=Count('product__category__name')).order_by('-purchase_count')

    most_popular_category_ = category_purchases.first()

    return most_popular_category_

def most_profitable_category():
    product_type_profit = Product.objects.annotate(
        total_profit=Sum('orders__price')).values('category__name', 'total_profit').order_by('-total_profit')

    most_profitable_product_cat = product_type_profit.first()

    return most_profitable_product_cat


def price_list(request):
    categories = Category.objects.all()

    category_product_prices = {}
    for category in categories:
        products = Product.objects.filter(category=category)
        product_list = [product.name for product in products]
        price_list_ = [product.price for product in products]
        category_product_prices[category.name] = {'products': product_list, 'prices': price_list_}

    most_popular_category_ = most_popular_category()
    most_profitable_category_ = most_profitable_category()

    return render(request, 'price_list.html', {'category_product_prices': category_product_prices,
                                               'most_popular_category': most_popular_category_,
                                               'most_profitable_category': most_profitable_category_})


from django.db.models import Sum

def customers(request):
    purchases = Purchase.objects.all()
    towns = []
    for purchase in purchases:
        if purchase.town not in towns:
            towns.append(purchase.town)

    towns_with_customers_info = {}
    for town in towns:
        purchases_by_town = Purchase.objects.filter(town=town)
        customers_info = []
        for purchase in purchases_by_town:
            customer = purchase.user.username
            total_purchase_amount = Purchase.objects.filter(user=purchase.user).aggregate(
                total_amount=Sum('order__price'))['total_amount'] or 0
            customers_info.append((customer, total_purchase_amount))
        towns_with_customers_info[town] = list(set(customers_info))

    customers_ = User.objects.filter(status='customer', is_superuser=False)

    ages = []
    for customer in customers_:
        ages.append(customer.age)

    average_age = sum(ages) / len(ages)
    median_age = median(ages)

    return render(request, 'customers.html', {'towns_with_customers_info': towns_with_customers_info,
                                              'average_age': average_age,
                                              'median_age': median_age
                                              })



def most_demanded_product():
    products_with_sold_count = Order.objects.values('product').annotate(sold_count=Sum('amount'))

    most_demanded_product_ = max(products_with_sold_count, key=lambda x: x['sold_count'])

    return Product.objects.get(pk=most_demanded_product_['product']), most_demanded_product_['sold_count']


def least_demanded_product():
    products_with_sold_count = Order.objects.values('product').annotate(sold_count=Sum('amount'))

    least_demanded_product_ = min(products_with_sold_count, key=lambda x: x['sold_count'])

    return Product.objects.get(pk=least_demanded_product_['product']), least_demanded_product_['sold_count']


def demand_analysis(request):
    most_demanded = most_demanded_product()
    least_demanded = least_demanded_product()
    return render(request, 'demand_analysis.html', {'most_demanded': most_demanded[0],
                                                    'most_demanded_sold': most_demanded[1],
                                                    'least_demanded': least_demanded[0],
                                                    'least_demanded_sold': least_demanded[1],
                                                    'most_demanded_profit': most_demanded[0].price * most_demanded[1],
                                                    'least_demanded_profit': least_demanded[0].price * least_demanded[1]})

def monthly_sales():
    sales_volume = Order.objects.annotate(month=TruncMonth('date')).values('product__category__name', 'month').annotate(
        total_sales=Sum('amount')).order_by('product__category__name', 'month')

    monthly_sales_ = {}
    for item in sales_volume:
        month = item['month'].strftime('%Y-%m')
        category = item['product__category__name']
        total_sales = item['total_sales']

        if month not in monthly_sales_:
            monthly_sales_[month] = {}

        monthly_sales_[month][category] = total_sales

    sorted_monthly_sales = dict(sorted(monthly_sales_.items()))

    return sorted_monthly_sales


def monthly_sales_volume(request):
    matplotlib.use('Agg')

    monthly_sales_ = monthly_sales()

    image_urls = []

    bar_colors = ['cyan', 'green', 'red', 'orange', 'purple', 'yellow']

    for month, sales in monthly_sales_.items():
        plt.figure(figsize=(16, 9))
        labels = list(sales.keys())
        values = list(sales.values())

        plt.bar(labels, values, color=bar_colors[:len(labels)])
        plt.xlabel('Category')
        plt.ylabel('Sales Volume')
        plt.title(f'Monthly Sales Volume - {month}')
        plt.xticks(rotation=45)
        plt.tight_layout()

        fig = plt.gcf()
        buf = io.BytesIO()
        fig.savefig(buf, format='png')
        buf.seek(0)
        string = base64.b64encode(buf.read())
        url = parse.quote(string)

        image_urls.append(url)

    return render(request, 'monthly_sales.html', {'images': image_urls})


def yearly_sales_report(year):
    purchases = Purchase.objects.filter(purchase_date__year=year)
    total_sales_per_purchase = purchases.annotate(total_sales=Sum('order__price')).values_list('total_sales', flat=True)
    total_sales_for_year = sum(total_sales_per_purchase)
    return total_sales_for_year


def yearly_sales_trend():
    current_year = datetime.now().year
    last_three_years = range(current_year - 2, current_year + 1)
    yearly_sales_ = []

    for year in last_three_years:
        sales = yearly_sales_report(year)
        yearly_sales_.append(round(sales, 2))

    return list(last_three_years), yearly_sales_


def linear_sales_trend(request):
    matplotlib.use('Agg')

    years, sales = yearly_sales_trend()

    trend_line = np.polyfit(years, sales, 1)
    trend_line_fn = np.poly1d(trend_line)

    next_year = years[-1] + 1
    next_sales = trend_line_fn(next_year)
    years.append(next_year)
    sales.append(round(next_sales, 2))

    plt.figure(figsize=(14, 9))
    plt.plot(years, sales, marker='o', linestyle='-')
    plt.xlabel('Year')
    plt.ylabel('Total Sales')
    plt.title('Yearly Sales Trend')
    plt.xticks(years)
    plt.grid(True)
    plt.tight_layout()

    fig = plt.gcf()
    buf = io.BytesIO()
    fig.savefig(buf, format='png')
    buf.seek(0)
    string = base64.b64encode(buf.read())
    url = parse.quote(string)

    yearly_sales_data = list(zip(years, sales))

    return render(request, 'linear_trend.html', {'image': url, 'yearly_sales_data': yearly_sales_data})
