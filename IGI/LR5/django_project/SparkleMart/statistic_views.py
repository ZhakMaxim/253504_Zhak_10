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


def price_list(request):
    categories = Category.objects.all()

    category_product_prices = {}
    for category in categories:
        products = Product.objects.filter(category=category)
        product_list = [product.name for product in products]
        price_list_ = [product.price for product in products]
        category_product_prices[category.name] = {'products': product_list, 'prices': price_list_}
    return render(request, 'price_list.html', {'category_product_prices': category_product_prices})


def customers(request):
    purchases = Purchase.objects.all()
    towns = []
    for purchase in purchases:
        if purchase.town not in towns:
            towns.append(purchase.town)

    towns_with_customers_usernames = {}
    for town in towns:
        purchases_by_town = Purchase.objects.filter(town=town)
        users = list(set(purchase.user.username for purchase in purchases_by_town))
        towns_with_customers_usernames[town] = users
    return render(request, 'customers.html', {'towns_with_customer_count': towns_with_customers_usernames})


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
                                                    'least_demanded_sold': least_demanded[1]})

from django.db.models.functions import TruncMonth

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

    return monthly_sales_


def monthly_sales_volume(request):
    matplotlib.use('Agg')
    monthly_sales_ = monthly_sales()

    image_urls = []

    for month, sales in monthly_sales_.items():
        plt.figure(figsize=(16, 9))
        labels = list(sales.keys())
        values = list(sales.values())

        plt.bar(labels, values, color='blue')
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


def yearly_sales(request):
    current_year = datetime.now().year
    yearly_sales_ = yearly_sales_report(current_year)
    context = {
        'year': current_year,
        'yearly_sales': yearly_sales_,
    }
    return render(request, 'yearly_sales.html', context)


def yearly_sales_trend():
    current_year = datetime.now().year
    last_three_years = range(current_year - 2, current_year + 1)
    yearly_sales_ = []

    for year in last_three_years:
        sales = yearly_sales_report(year)
        yearly_sales_.append(sales)

    return list(last_three_years), yearly_sales_


def linear_sales_trend(request):
    years, sales = yearly_sales_trend()

    trend_line = np.polyfit(years, sales, 1)
    trend_line_fn = np.poly1d(trend_line)

    next_year = years[-1] + 1
    next_sales = trend_line_fn(next_year)
    years.append(next_year)
    sales.append(next_sales)

    plt.figure(figsize=(10, 6))
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

    return render(request, 'linear_trend.html', {'image': url})

