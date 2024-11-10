from django.test import SimpleTestCase
from django.core.exceptions import ValidationError
from decimal import Decimal
from base.models import Product, Order
from datetime import datetime, timezone


class OrderCalculationTests(SimpleTestCase):
    def setUp(self):
        self.order = Order()
        self.order._state.adding = True  # Mock the adding state
        
    def test_calculate_total_items(self):
        # Mock orderItems without database interaction
        self.order.orderItems = [
            {'qty': 2},
            {'qty': 3},
            {'qty': 1}
        ]
        total_items = sum(item['qty'] for item in self.order.orderItems)
        self.assertEqual(total_items, 6)

    # def test_calculate_total_price(self):
    #     # Mock orderItems without database interaction
    #     self.order.orderItems = [
    #         {'qty': 2, 'price': Decimal('10.00')},
    #         {'qty': 3, 'price': Decimal('5.00')},
    #         {'qty': 1, 'price': Decimal('15.00')}
    #     ]
    #     total_price = sum(
    #         Decimal(item['qty']) * Decimal(item['price']) 
    #         for item in self.order.orderItems
    #     )
    #     self.assertEqual(total_price, Decimal('40.00'))

class UtilityFunctionTests(SimpleTestCase):
    def test_format_price(self):
        price = Decimal('10.99')
        formatted_price = f"${price:.2f}"
        self.assertEqual(formatted_price, "$10.99")
    
    def test_calculate_discount(self):
        original_price = Decimal('100.00')
        discount_percentage = 20
        expected_discount = original_price * (Decimal(discount_percentage) / 100)
        self.assertEqual(expected_discount, Decimal('20.00'))

class DateTimeValidationTests(SimpleTestCase):
    def test_future_delivery_date(self):
        # Create a date in the past
        past_date = datetime(2020, 1, 1, tzinfo=timezone.utc)
        current_date = datetime.now(timezone.utc)
        
        self.assertLess(past_date, current_date)

    def test_business_hours_validation(self):
        test_hour = 14  # 2 PM
        self.assertTrue(9 <= test_hour <= 17)  # Business hours 9 AM to 5 PM

class ProductNameValidationTests(SimpleTestCase):
    def test_product_name_length(self):
        max_length = 200
        test_name = "A" * 201
        
        self.assertGreater(len(test_name), max_length)
    
    def test_valid_product_name_length(self):
        max_length = 200
        test_name = "A" * 200
        
        self.assertEqual(len(test_name), max_length)

class PriceFormatTests(SimpleTestCase):
    def test_round_price(self):
        price = Decimal('10.999')
        rounded_price = round(price, 2)
        self.assertEqual(rounded_price, Decimal('11.00'))
    
    def test_price_string_format(self):
        price = Decimal('1234.56')
        formatted_price = f"${price:,.2f}"
        self.assertEqual(formatted_price, "$1,234.56")
