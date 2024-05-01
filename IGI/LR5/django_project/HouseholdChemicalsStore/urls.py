"""
URL configuration for HouseholdChemicalsStore project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.contrib import admin
from django.urls import path, re_path

from django.conf import settings
from django.conf.urls.static import static

from SparkleMart import views
from SparkleMart import statistic_views


urlpatterns = [
    path('home/', views.home, name='home'),
    path('about/', views.about_company, name='about'),
    path('news/', views.news, name='news'),
    path('terms/', views.terms, name='terms'),
    path('contacts/', views.contacts, name='contacts'),
    path('vacancies/', views.vacancies, name='vacancies'),
    path('reviews/', views.ReviewListView.as_view(), name='reviews'),
    path('add_review/', views.ReviewCreateView.as_view(), name='add_review'),
    path('privacy-policy/', views.privacy_policy, name='privacy_policy'),
    path('random_fact/', views.random_fact, name='random_fact'),
    path('random_joke/', views.random_joke, name='random_joke'),

    path('price_list', statistic_views.price_list, name='price_list'),
    path('customers', statistic_views.customers, name='customers'),
    path('demand_analysis', statistic_views.demand_analysis, name='demand_analysis'),
    path('monthly_sales_volume', statistic_views.monthly_sales_volume, name='monthly_sales_volume'),
    path('yearly_sales', statistic_views.yearly_sales, name='yearly_sales'),
    path('linear_trend', statistic_views.linear_sales_trend, name='linear_trend'),

    path('admin/', admin.site.urls),
    path('register/', views.UserRegistrationView.as_view(), name='register'),
    path('login/', views.UserAuthorizationView.as_view(), name='login'),
    path('logout/', views.UserLogoutView.as_view(), name='logout'),
    path('profile/', views.profile, name='profile'),
    path('products/', views.ProductListView.as_view(), name='products'),
    re_path(r'products/(?P<pk>\d+)/$', views.ProductDetailView.as_view(), name='product'),
    re_path(r'products/(?P<pk>\d+)/order/create/', views.OrderCreateView.as_view(), name='create_order'),
    path('orders/', views.OrderListView.as_view(), name='orders'),
    re_path(r'orders/(?P<pk>\d+)/$', views.OrderDeleteDetailView.as_view(), name='order'),
    path('users/', views.UserListView.as_view(), name='users'),
    re_path(r'users/(?P<pk>\d+)/$', views.UserDetailView.as_view(), name='user'),
    re_path(r'user/(?P<pk>\d+)/orders/', views.UserOrderListView.as_view(), name='user_orders'),
    re_path(r'orders/(?P<pk>\d+)/purchase/create/', views.PurchaseCreateView.as_view(), name='create_purchase'),
    path('purchases/', views.PurchaseListView.as_view(), name='purchases'),
    re_path(r'purchases/(?P<pk>\d+)/$', views.PurchaseDetailView.as_view(), name='purchase'),
    path('promos/', views.PromoListView.as_view(), name='promos'),
    path('pick_up_points/', views.PickUpPointListView.as_view(), name='pick_up_points'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)
