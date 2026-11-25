import unittest
from decimal import Decimal

from order_calculator import (
    calculate_subtotal,
    apply_regular_customer_discount,
    calculate_delivery_cost,
    apply_promo_code,
    calculate_order_total,
)


class TestOrderCalculator(unittest.TestCase):

    def setUp(self):
        self.items = [
            {
                "name": "Керамічна чашка",
                "price": 350,
                "quantity": 2,
            },
            {
                "name": "Ароматична свічка",
                "price": 280,
                "quantity": 1,
            },
        ]

    def test_calculate_subtotal(self):
        result = calculate_subtotal(self.items)
        self.assertEqual(result, Decimal("980.00"))

    def test_regular_customer_discount(self):
        result = apply_regular_customer_discount(
            Decimal("980.00"),
            True,
        )
        self.assertEqual(result, Decimal("882.00"))

    def test_delivery_cost_for_lviv(self):
        result = calculate_delivery_cost(
            Decimal("882.00"),
            "Lviv",
        )
        self.assertEqual(result, Decimal("50.00"))

    def test_free_delivery(self):
        result = calculate_delivery_cost(
            Decimal("1500.00"),
            "Lviv",
        )
        self.assertEqual(result, Decimal("0.00"))

    def test_craft10_promo_code(self):
        result = apply_promo_code(
            Decimal("932.00"),
            "CRAFT10",
        )
        self.assertEqual(result, Decimal("838.80"))

    def test_complete_order_total(self):
        result = calculate_order_total(
            items=self.items,
            is_regular_customer=True,
            delivery_region="Lviv",
            payment_method="card",
            promo_code="CRAFT10",
        )

        self.assertEqual(
            result["subtotal"],
            Decimal("980.00"),
        )

        self.assertEqual(
            result["discounted_subtotal"],
            Decimal("882.00"),
        )

        self.assertEqual(
            result["delivery_cost"],
            Decimal("50.00"),
        )

        self.assertEqual(
            result["total"],
            Decimal("838.80"),
        )

    def test_empty_cart_raises_error(self):
        with self.assertRaises(ValueError):
            calculate_order_total(
                items=[],
                is_regular_customer=False,
                delivery_region="Lviv",
                payment_method="card",
            )

    def test_negative_quantity_raises_error(self):
        invalid_items = [
            {
                "name": "Керамічна чашка",
                "price": 350,
                "quantity": -1,
            }
        ]

        with self.assertRaises(ValueError):
            calculate_order_total(
                items=invalid_items,
                is_regular_customer=False,
                delivery_region="Lviv",
                payment_method="card",
            )


if __name__ == "__main__":
    unittest.main()