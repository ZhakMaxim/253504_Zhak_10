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
from django.urls import path
from SparkleMart import views

from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('home/', views.home, name='home'),
    path('about/', views.about_company, name='about'),
    path('news/', views.news, name='news'),
    path('terms/', views.terms, name='terms'),
    path('contacts/', views.contacts, name='contacts'),
    path('vacancies/', views.vacancies, name='vacancies'),
    path('reviews/', views.reviews, name='reviews'),
    path('privacy-policy', views.privacy_policy, name='privacy_policy'),

    path('admin/', admin.site.urls),
    path('register/', views.UserRegistrationView.as_view(), name='register'),
    path('login/', views.UserAuthorizationView.as_view(), name='login'),
    path('logout/', views.UserLogoutView.as_view(), name='logout'),
    path('products/', views.ProductListView.as_view(), name='products'),
    path('products/<int:pk>/', views.ProductDetailView.as_view(), name='product'),
    path('products/<int:pk>/order/create/', views.OrderCreateView.as_view(), name='create_order'),
    path('orders/', views.OrderListView.as_view(), name='orders'),
    path('orders/<int:pk>/', views.OrderDetailView.as_view(), name='order'),
    path('orders/<int:pk>/delete/', views.OrderDeleteView.as_view(), name='order_delete'),
    path('users/', views.UserListView.as_view(), name='users'),
    path('users/<int:pk>/', views.UserDetailView.as_view(), name='user'),
    path('user/<int:pk>/orders/', views.UserOrderListView.as_view(), name='user_orders'),
    path('orders/<int:pk>/purchase/create/', views.PurchaseCreateView.as_view(), name='create_purchase'),
    path('purchases/', views.PurchaseListView.as_view(), name='purchases'),
    path('purchases/<int:pk>/', views.PurchaseDetailView.as_view(), name='purchase'),
    path('promos/', views.PromoListView.as_view(), name='promos'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)
