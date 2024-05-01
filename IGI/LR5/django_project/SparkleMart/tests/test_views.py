from django.test import TestCase, Client
from django.urls import reverse

from SparkleMart.views import *

from datetime import datetime
from django.utils import timezone

datetime.now(tz=timezone.utc)

class ReviewListViewTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        number_of_reviews = 5

        for review_num in range(number_of_reviews):
            Review.objects.create(name=f'review{review_num}', rating=3, text=f'text{review_num}', date=datetime.now())

    def test_lists_all_reviews(self):
        resp = self.client.get(reverse('reviews'))
        self.assertEqual(resp.status_code, 200)
        self.assertTrue(len(resp.context['review_list']) == 5)


class ReviewCreateViewTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username='testuser', email='test@gmail.com', password='password',
                                             age=18, phone_number='+375291234567', status='customer')
        self.client.login(username='testuser', password='password')
        self.valid_data = {
            'name': 'Test Review',
            'rating': 5,
            'text': 'This is a test review.',
        }
        self.invalid_data = {
            'name': '',
            'rating': 6,
            'text': '',
        }

    def test_get_authenticated_customer(self):
        response = self.client.get(reverse('add_review'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'add_review.html')
        self.assertIsInstance(response.context['form'], ReviewForm)

    def test_get_unauthenticated(self):
        self.client.logout()
        response = self.client.get(reverse('add_review'))
        self.assertEqual(response.status_code, 302)

    def test_post_authenticated_customer_valid_data(self):
        response = self.client.post(reverse('add_review'), data=self.valid_data)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(Review.objects.count(), 1)

    def test_post_authenticated_customer_invalid_data(self):
        response = self.client.post(reverse('add_review'), data=self.invalid_data)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(Review.objects.count(), 0)

    def test_post_unauthenticated(self):
        self.client.logout()
        response = self.client.post(reverse('add_review'), data=self.valid_data)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(Review.objects.count(), 0)


class UserRegistrationViewTestCase(TestCase):
    def setUp(self):
        self.client = Client()
        self.valid_data = {
            'username': 'testuser',
            'email': 'test@gmail.com',
            'phone_number': '+375291234567',
            'age': 20,
            'password1': 'password123',
            'password2': 'password123',
        }
        self.invalid_data = {
            'username': '',
            'password1': 'password',  # too short
            'password2': 'password',  # too short
            'email': 'testgmail.com',  # invalid email
            'phone_number': '1234567890',  # invalid phone number format
            'age': 17,  # too young
        }

    def test_get(self):
        response = self.client.get(reverse('register'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'register.html')
        self.assertIsInstance(response.context['form'], RegistrationForm)

    def test_post_valid_data(self):
        response = self.client.post(reverse('register'), data=self.valid_data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(User.objects.count(), 0)  # new user created

    def test_post_invalid_data(self):
        response = self.client.post(reverse('register'), data=self.invalid_data)
        self.assertEqual(response.status_code, 200)  # form should be rendered again
        self.assertEqual(User.objects.count(), 0)  # no user should be created


class UserAuthorizationViewTestCase(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username='testuser', email='test@gmail.com', password='password',
                                             age=18, phone_number='+375291234567', status='customer')
        self.valid_credentials = {
            'username': 'testuser',
            'password': 'password',
        }
        self.invalid_credentials = {
            'username': 'testuser',
            'password': 'wrongpassword',
        }

    def test_get(self):
        response = self.client.get(reverse('login'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'login.html')

    def test_post_valid_credentials(self):
        response = self.client.post(reverse('login'), data=self.valid_credentials)
        self.assertEqual(response.status_code, 302)  # redirected to 'home' page

    def test_post_invalid_credentials(self):
        response = self.client.post(reverse('login'), data=self.invalid_credentials)
        self.assertEqual(response.status_code, 200)  # form should be rendered again
        self.assertContains(response, "Please enter a correct username and password.")


class UserLogoutViewTestCase(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username='testuser', email='test@gmail.com', password='password',
                                             age=18, phone_number='+375291234567', status='customer')
        self.client.login(username='testuser', password='password')

    def test_logout_authenticated_user(self):
        response = self.client.get(reverse('logout'))
        self.assertEqual(response.status_code, 302)  # redirected to 'home' page
        self.assertFalse(response.wsgi_request.user.is_authenticated)  # user should be logged out

    def test_logout_unauthenticated_user(self):
        self.client.logout()
        response = self.client.get(reverse('logout'))
        self.assertEqual(response.status_code, 302)


class UserListViewTestCase(TestCase):
    def setUp(self):
        self.client = Client()

        self.employee_user = User.objects.create_user(username='employee', email='test@gmail.com', password='password',
                                                      age=18, phone_number='+375291234567', status='employee')

        self.customer_user1 = User.objects.create_user(username='customer1', email='test@gmail.com',
                                                       password='password',
                                                       age=18, phone_number='+375291234567', status='customer')
        self.customer_user2 = User.objects.create_user(username='customer2', email='test@gmail.com',
                                                       password='password',
                                                       age=18, phone_number='+375291234567', status='customer')

    def test_get_authenticated_employee(self):
        self.client.login(username='employee', password='password')
        response = self.client.get(reverse('users'))
        self.assertEqual(response.status_code, 200)
        users_data = response.json()
        self.assertEqual(len(users_data), 2)

        self.assertDictEqual(users_data[0], {
            "id": self.customer_user1.id,
            "username": "customer1",
            "phone_number": "+375291234567",
            "email": "test@gmail.com",
        })
        self.assertDictEqual(users_data[1], {
            "id": self.customer_user2.id,
            "username": "customer2",
            "phone_number": "+375291234567",
            "email": "test@gmail.com",
        })

    def test_get_unauthenticated(self):
        response = self.client.get(reverse('users'))
        self.assertEqual(response.status_code, 404)


class UserDetailViewTestCase(TestCase):
    def setUp(self):
        self.client = Client()
        self.employee_user = User.objects.create_user(username='employee', email='test@gmail.com', password='password',
                                                      age=18, phone_number='+375291234567', status='employee')

        self.customer_user = User.objects.create_user(username='customer', email='test@gmail.com',
                                                      password='password',
                                                      age=18, phone_number='+375291234567', status='customer')

    def test_get_authenticated_employee(self):
        self.client.login(username='employee', password='password')
        response = self.client.get(reverse('user', kwargs={'pk': self.customer_user.pk}))
        self.assertEqual(response.status_code, 200)
        user_data = response.json()
        self.assertEqual(user_data["id"], self.customer_user.id)
        self.assertEqual(user_data["username"], "customer")
        self.assertEqual(user_data["phone_number"], "+375291234567")
        self.assertEqual(user_data["email"], "test@gmail.com")

    def test_get_unauthenticated(self):
        response = self.client.get(reverse('user', kwargs={'pk': self.customer_user.pk}))
        self.assertEqual(response.status_code, 404)

    def test_get_authenticated_employee_invalid_pk(self):
        self.client.login(username='employee', password='password')
        response = self.client.get(reverse('user', kwargs={'pk': self.employee_user.pk}))
        self.assertEqual(response.status_code, 404)


class ProductListViewTestCase(TestCase):
    def setUp(self):
        self.client = Client()

        self.category = Category.objects.create(name='TestCategory')
        self.producer = Producer.objects.create(name='TestProducer')

        self.product1 = Product.objects.create(name='Product1', price=10, amount=5, producer=self.producer)
        self.product1.category.add(self.category)
        self.product2 = Product.objects.create(name='Product2', price=20, amount=10, producer=self.producer)
        self.product2.category.add(self.category)

    def test_get_all_products(self):
        response = self.client.get(reverse('products'))
        self.assertEqual(response.status_code, 200)
        products_data = response.json()
        self.assertEqual(len(products_data), 2)

    def test_filter_products_by_category(self):
        response = self.client.get(reverse('products'), {'category_id': self.category.pk})
        self.assertEqual(response.status_code, 200)
        products_data = response.json()
        self.assertEqual(len(products_data), 2)

    def test_filter_products_by_price_range(self):
        response = self.client.get(reverse('products'), {'min_price': 15, 'max_price': 25})
        self.assertEqual(response.status_code, 200)
        products_data = response.json()
        self.assertEqual(len(products_data), 1)
        self.assertEqual(products_data[0]['name'], 'Product2')


class ProductDetailViewTestCase(TestCase):
    def setUp(self):
        self.client = Client()

        self.category = Category.objects.create(name='TestCategory')
        self.producer = Producer.objects.create(name='TestProducer')

        self.product = Product.objects.create(name='Product', price=10, amount=10, producer=self.producer)
        self.product.category.add(self.category)

    def test_get_existing_product(self):
        response = self.client.get(reverse('product', kwargs={'pk': self.product.pk}))
        self.assertEqual(response.status_code, 200)
        product_data = response.json()
        self.assertEqual(product_data['name'], 'Product')

    def test_get_non_existing_product(self):
        response = self.client.get(reverse('product', kwargs={'pk': 999}))
        self.assertEqual(response.status_code, 404)


class OrderCreateViewTestCase(TestCase):
    def setUp(self):
        self.client = Client()
        self.employee_user = User.objects.create_user(username='customer', email='test@gmail.com', password='password',
                                                      age=18, phone_number='+375291234567', status='customer')

        self.producer = Producer.objects.create(name='TestProducer')

        self.product = Product.objects.create(name='Product', price=10, amount=5, producer=self.producer)

    def test_get_authenticated_customer_valid_product(self):
        self.client.login(username='customer', password='password')
        response = self.client.get(reverse('create_order', kwargs={'pk': self.product.pk}))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'order_form.html')

    def test_get_authenticated_customer_invalid_product(self):
        self.client.login(username='customer', password='password')
        response = self.client.get(reverse('create_order', kwargs={'pk': 999}))
        self.assertEqual(response.status_code, 404)

    def test_get_unauthenticated(self):
        response = self.client.get(reverse('create_order', kwargs={'pk': self.product.pk}))
        self.assertEqual(response.status_code, 404)

    def test_post_authenticated_customer_valid_data(self):
        self.client.login(username='customer', password='password')
        response = self.client.post(reverse('create_order', kwargs={'pk': self.product.pk}), {'amount': 3})
        self.assertEqual(response.status_code, 200)
        order_data = response.json()
        self.assertEqual(order_data['user'], 'customer')
        self.assertEqual(order_data['product_id'], self.product.id)
        self.assertEqual(order_data['amount'], 3)
        self.assertEqual(Order.objects.count(), 1)

    def test_post_authenticated_customer_invalid_data(self):
        self.client.login(username='customer', password='password')
        response = self.client.post(reverse('create_order', kwargs={'pk': self.product.pk}), {'amount': 10})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.content.decode('utf-8'), 'There are not enough products in stock to place an order')
        self.assertEqual(Order.objects.count(), 0)

    def test_post_authenticated_employee(self):
        self.client.login(username='employee', password='password')
        response = self.client.post(reverse('create_order', kwargs={'pk': self.product.pk}), {'amount': 3})
        self.assertEqual(response.status_code, 200)

    def test_post_unauthenticated(self):
        response = self.client.post(reverse('create_order', kwargs={'pk': self.product.pk}))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.content.decode('utf-8'), 'please, login for making order!')
        self.assertEqual(Order.objects.count(), 0)


class OrderListViewTestCase(TestCase):
    def setUp(self):
        self.client = Client()
        self.employee_user = User.objects.create_user(username='employee', email='test@gmail.com', password='password',
                                                      age=18, phone_number='+375291234567', status='employee')

        self.producer = Producer.objects.create(name='TestProducer')
        self.product = Product.objects.create(name='Product', price=10, amount=5, producer=self.producer)

        self.order1 = Order.objects.create(user=self.employee_user, number='12345', price=10, amount=2, product_id=1)
        self.order2 = Order.objects.create(user=self.employee_user, number='67890', price=20, amount=1, product_id=1)

    def test_get_authenticated_employee(self):
        self.client.login(username='employee', password='password')
        response = self.client.get(reverse('user_orders', kwargs={'pk': self.employee_user.pk}))
        self.assertEqual(response.status_code, 200)
        orders_data = response.json()
        self.assertEqual(len(orders_data), 2)

    def test_get_unauthenticated(self):
        response = self.client.get(reverse('user_orders', kwargs={'pk': self.employee_user.pk}))
        self.assertEqual(response.status_code, 404)


class OrderDeleteDetailViewTestCase(TestCase):
    def setUp(self):
        self.client = Client()
        self.employee_user = User.objects.create_user(username='employee', email='test@gmail.com', password='password',
                                                      age=18, phone_number='+375291234567', status='employee')
        self.customer_user = User.objects.create_user(username='customer', email='test@gmail.com', password='password',
                                                      age=18, phone_number='+375291234567', status='customer')

        self.producer = Producer.objects.create(name='TestProducer')
        self.product = Product.objects.create(name='Product', price=10, amount=5, producer=self.producer)

        self.order1 = Order.objects.create(user=self.employee_user, number='12345', price=10, amount=2, product_id=1)
        self.order2 = Order.objects.create(user=self.customer_user, number='67890', price=20, amount=1, product_id=1)

    def test_get_authenticated_employee_valid_order(self):
        self.client.login(username='employee', password='password')
        response = self.client.get(reverse('order', kwargs={'pk': self.order1.pk}))
        self.assertEqual(response.status_code, 200)
        order_data = response.json()
        self.assertEqual(order_data['user'], 'employee')
        self.assertEqual(order_data['number'], 12345)

    def test_get_authenticated_employee_invalid_order(self):
        self.client.login(username='employee', password='password')
        response = self.client.get(reverse('order', kwargs={'pk': 999}))
        self.assertEqual(response.status_code, 404)

    def test_get_authenticated_customer_own_order(self):
        self.client.login(username='customer', password='password')
        response = self.client.get(reverse('order', kwargs={'pk': self.order2.pk}))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'order_detail.html')

    def test_get_authenticated_customer_other_order(self):
        self.client.login(username='customer', password='password')
        response = self.client.get(reverse('order', kwargs={'pk': self.order1.pk}))
        self.assertEqual(response.status_code, 404)

    def test_post_authenticated_customer_invalid_data(self):
        self.client.login(username='customer', password='password')
        response = self.client.post(reverse('order', kwargs={'pk': self.order2.pk}), {'confirm': False})
        self.assertEqual(response.status_code, 404)


class UserOrderListViewTestCase(TestCase):
    def setUp(self):
        self.client = Client()
        self.employee_user = User.objects.create_user(username='employee', email='test@gmail.com', password='password',
                                                      age=18, phone_number='+375291234567', status='customer')
        self.customer_user = User.objects.create_user(username='customer', email='test@gmail.com', password='password',
                                                      age=18, phone_number='+375291234567', status='customer')

        self.producer = Producer.objects.create(name='TestProducer')
        self.product = Product.objects.create(name='Product', price=10, amount=5, producer=self.producer)

        self.order1 = Order.objects.create(user=self.customer_user, number='12345', price=10, amount=2, product_id=1)
        self.order2 = Order.objects.create(user=self.customer_user, number='67890', price=20, amount=1, product_id=1)

    def test_get_authenticated_employee_valid_user_orders(self):
        self.client.login(username='customer', password='password')
        response = self.client.get(reverse('user_orders', kwargs={'pk': self.customer_user.pk}))
        self.assertEqual(response.status_code, 200)
        orders_data = response.json()
        self.assertEqual(len(orders_data), 2)
        self.assertEqual(orders_data[0]['number'], 12345)

    def test_get_authenticated_employee_invalid_user_orders(self):
        self.client.login(username='employee', password='password')
        response = self.client.get(reverse('user_orders', kwargs={'pk': self.customer_user.pk}))
        self.assertEqual(response.status_code, 404)

    def test_get_authenticated_customer_own_orders(self):
        self.client.login(username='customer', password='password')
        response = self.client.get(reverse('user_orders', kwargs={'pk': self.customer_user.pk}))
        self.assertEqual(response.status_code, 200)
        orders_data = response.json()
        self.assertEqual(len(orders_data), 2)
        self.assertEqual(orders_data[1]['number'], 67890)

    def test_get_unauthenticated(self):
        response = self.client.get(reverse('user_orders', kwargs={'pk': self.customer_user.pk}))
        self.assertEqual(response.status_code, 404)


class PurchaseCreateViewTestCase(TestCase):
    def setUp(self):
        self.client = Client()
        self.customer_user = User.objects.create_user(username='customer', email='test@gmail.com', password='password',
                                                      age=18, phone_number='+375291234567', status='customer')

        self.producer = Producer.objects.create(name='TestProducer')
        self.product = Product.objects.create(name='Product', price=10, amount=5, producer=self.producer)

        self.order = Order.objects.create(user=self.customer_user, number='12345', price=10, amount=2, product_id=1)

        self.promo = Promo.objects.create(code='TESTCODE', discount=5)

    def test_get_authenticated_customer_valid_order(self):
        self.client.login(username='customer', password='password')
        response = self.client.get(reverse('create_purchase', kwargs={'pk': self.order.pk}))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'purchase_form.html')

    def test_get_authenticated_customer_invalid_order(self):
        self.client.login(username='customer', password='password')
        response = self.client.get(reverse('create_purchase', kwargs={'pk': 999}))
        self.assertEqual(response.status_code, 404)

    def test_post_authenticated_customer_valid_data_with_promo(self):
        self.client.login(username='customer', password='password')
        response = self.client.post(reverse('create_purchase', kwargs={'pk': self.order.pk}), {'town': 'TestTown',
                                                                                               'promo_code': 'TESTCODE'})
        self.assertEqual(response.status_code, 200)
        purchase_data = response.json()
        self.assertEqual(purchase_data['order_id'], 12345)
        self.assertEqual(purchase_data['user_id'], self.customer_user.id)
        self.assertEqual(purchase_data['town'], 'TestTown')
        self.assertEqual(Purchase.objects.count(), 1)
        self.assertEqual(Order.objects.get(pk=self.order.pk).is_active, False)

    def test_post_authenticated_customer_invalid_data(self):
        self.client.login(username='customer', password='password')
        response = self.client.post(reverse('create_purchase', kwargs={'pk': self.order.pk}), {})
        self.assertEqual(response.status_code, 404)

    def test_post_unauthenticated(self):
        response = self.client.post(reverse('create_purchase', kwargs={'pk': self.order.pk}))
        self.assertEqual(response.status_code, 404)


class PurchaseListViewTestCase(TestCase):
    def setUp(self):
        self.client = Client()

        self.employee_user = User.objects.create_user(username='employee', email='test@gmail.com', password='password',
                                                      age=18, phone_number='+375291234567', status='employee')

        self.producer = Producer.objects.create(name='TestProducer')
        self.product = Product.objects.create(name='Product', price=10, amount=5, producer=self.producer)

        self.order1 = Order.objects.create(user=self.employee_user, price=20, amount=2, product_id=1)
        self.order2 = Order.objects.create(user=self.employee_user, price=10, amount=1, product_id=1)

        self.purchase1 = Purchase.objects.create(order_id=1, town='Town1',
                                                 delivery_date=datetime(2024, 5, 1, 17, 0, 0, 0), user_id=1)
        self.purchase2 = Purchase.objects.create(order_id=2, town='Town2',
                                                 delivery_date=datetime(2024, 5, 1, 17, 0, 0, 0), user_id=1)

    def test_get_authenticated_employee(self):
        self.client.login(username='employee', password='password')
        response = self.client.get(reverse('purchases'))
        self.assertEqual(response.status_code, 200)
        purchases_data = response.json()
        self.assertEqual(len(purchases_data), 2)

    def test_get_unauthenticated(self):
        response = self.client.get(reverse('purchases'))
        self.assertEqual(response.status_code, 404)


class PurchaseDetailViewTestCase(TestCase):
    def setUp(self):
        self.client = Client()
        self.employee_user = User.objects.create_user(username='employee', email='test@gmail.com', password='password',
                                                      age=18, phone_number='+375291234567', status='employee')

        self.customer_user = User.objects.create_user(username='customer', email='test@gmail.com', password='password',
                                                      age=18, phone_number='+375291234567', status='customer')

        self.producer = Producer.objects.create(name='TestProducer')
        self.product = Product.objects.create(name='Product', price=10, amount=5, producer=self.producer)

        self.order1 = Order.objects.create(user=self.employee_user, price=20, amount=2, product_id=1)
        self.order2 = Order.objects.create(user=self.employee_user, price=10, amount=1, product_id=1)

        self.purchase1 = Purchase.objects.create(order_id=1, town='Town1',
                                                 delivery_date=datetime(2024, 5, 1, 17, 0, 0, 0), user_id=1)
        self.purchase2 = Purchase.objects.create(order_id=2, town='Town2',
                                                 delivery_date=datetime(2024, 5, 1, 17, 0, 0, 0), user_id=2)

    def test_get_authenticated_employee_valid_purchase(self):
        self.client.login(username='employee', password='password')
        response = self.client.get(reverse('purchase', kwargs={'pk': self.purchase1.pk}))
        self.assertEqual(response.status_code, 200)
        purchase_data = response.json()
        self.assertEqual(purchase_data['order_id'], 1)
        self.assertEqual(purchase_data['town'], 'Town1')

    def test_get_authenticated_employee_invalid_purchase(self):
        self.client.login(username='employee', password='password')
        response = self.client.get(reverse('purchase', kwargs={'pk': 999}))
        self.assertEqual(response.status_code, 404)

    def test_get_authenticated_customer_own_purchase(self):
        self.client.login(username='customer', password='password')
        response = self.client.get(reverse('purchase', kwargs={'pk': self.purchase2.pk}))
        self.assertEqual(response.status_code, 200)
        purchase_data = response.json()
        self.assertEqual(purchase_data['order_id'], 2)
        self.assertEqual(purchase_data['town'], 'Town2')

    def test_get_authenticated_customer_other_purchase(self):
        self.client.login(username='customer', password='password')
        response = self.client.get(reverse('purchase', kwargs={'pk': self.purchase1.pk}))
        self.assertEqual(response.status_code, 404)

    def test_get_unauthenticated(self):
        response = self.client.get(reverse('purchase', kwargs={'pk': self.purchase1.pk}))
        self.assertEqual(response.status_code, 404)


class PromoListViewTestCase(TestCase):
    def setUp(self):
        self.client = Client()
        Promo.objects.create(code='PROMO1', discount=10)
        Promo.objects.create(code='PROMO2', discount=20)

    def test_get_promo_list(self):
        response = self.client.get(reverse('promos'))
        self.assertEqual(response.status_code, 200)
        promos_data = response.json()
        self.assertEqual(len(promos_data), 2)
        self.assertEqual(promos_data[0]['code'], 'PROMO1')
        self.assertEqual(promos_data[0]['discount'], 10)
        self.assertEqual(promos_data[1]['code'], 'PROMO2')
        self.assertEqual(promos_data[1]['discount'], 20)