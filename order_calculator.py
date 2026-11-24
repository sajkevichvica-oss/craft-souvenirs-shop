from decimal import Decimal, ROUND_HALF_UP


REGULAR_CUSTOMER_DISCOUNT = Decimal("0.10")
PROMO_CODE_DISCOUNT = Decimal("0.10")
FIXED_PROMO_DISCOUNT = Decimal("50.00")
FREE_DELIVERY_THRESHOLD = Decimal("1500.00")

DELIVERY_COSTS = {
    "Lviv": Decimal("50.00"),
    "Ukraine": Decimal("80.00"),
    "International": Decimal("150.00"),
}

VALID_PAYMENT_METHODS = {"card", "cash"}


def round_money(value):
    """Округлює грошове значення до двох знаків."""
    return value.quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)


def validate_items(items):
    """Перевіряє правильність товарів у кошику."""
    if not items:
        raise ValueError("Кошик не може бути порожнім.")

    for item in items:
        required_fields = {"name", "price", "quantity"}

        if not required_fields.issubset(item):
            raise ValueError(
                "Кожний товар повинен містити name, price і quantity."
            )

        price = Decimal(str(item["price"]))
        quantity = item["quantity"]

        if price <= 0:
            raise ValueError(
                f"Ціна товару '{item['name']}' повинна бути більшою за нуль."
            )

        if not isinstance(quantity, int) or quantity <= 0:
            raise ValueError(
                f"Кількість товару '{item['name']}' повинна бути "
                "цілим числом, більшим за нуль."
            )


def calculate_subtotal(items):
    """Обчислює загальну вартість товарів."""
    subtotal = Decimal("0.00")

    for item in items:
        price = Decimal(str(item["price"]))
        quantity = item["quantity"]
        subtotal += price * quantity

    return round_money(subtotal)


def apply_regular_customer_discount(
    subtotal,
    is_regular_customer
):
    """Застосовує знижку постійного покупця."""
    if not is_regular_customer:
        return subtotal

    discount = subtotal * REGULAR_CUSTOMER_DISCOUNT
    return round_money(subtotal - discount)


def calculate_delivery_cost(
    discounted_subtotal,
    delivery_region
):
    """Визначає вартість доставки."""
    if discounted_subtotal >= FREE_DELIVERY_THRESHOLD:
        return Decimal("0.00")

    if delivery_region not in DELIVERY_COSTS:
        raise ValueError(
            f"Непідтримуваний регіон доставки: {delivery_region}"
        )

    return DELIVERY_COSTS[delivery_region]


def apply_promo_code(total, promo_code):
    """Застосовує промокод до загальної суми."""
    if not promo_code:
        return total

    if promo_code == "CRAFT10":
        discount = total * PROMO_CODE_DISCOUNT
        return round_money(total - discount)

    if promo_code == "SAVE50":
        return round_money(
            max(Decimal("0.00"), total - FIXED_PROMO_DISCOUNT)
        )

    raise ValueError("Невідомий промокод.")


def calculate_order_total(
    items,
    is_regular_customer,
    delivery_region,
    payment_method,
    promo_code=""
):
    """Обчислює підсумкову вартість замовлення."""
    validate_items(items)

    if payment_method not in VALID_PAYMENT_METHODS:
        raise ValueError("Непідтримуваний спосіб оплати.")

    subtotal = calculate_subtotal(items)

    discounted_subtotal = apply_regular_customer_discount(
        subtotal,
        is_regular_customer
    )

    delivery_cost = calculate_delivery_cost(
        discounted_subtotal,
        delivery_region
    )

    total_before_promo = discounted_subtotal + delivery_cost

    total = apply_promo_code(
        total_before_promo,
        promo_code
    )

    return {
        "subtotal": subtotal,
        "discounted_subtotal": discounted_subtotal,
        "delivery_cost": delivery_cost,
        "total": total,
    }


def main():
    """Запускає приклад розрахунку замовлення."""
    items = [
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

    try:
        order_summary = calculate_order_total(
            items=items,
            is_regular_customer=True,
            delivery_region="Lviv",
            payment_method="card",
            promo_code="CRAFT10",
        )

        print(
            f"Вартість товарів: "
            f"{order_summary['subtotal']} грн"
        )
        print(
            f"Після знижки покупця: "
            f"{order_summary['discounted_subtotal']} грн"
        )
        print(
            f"Доставка: "
            f"{order_summary['delivery_cost']} грн"
        )
        print(
            f"До сплати: "
            f"{order_summary['total']} грн"
        )

    except ValueError as error:
        print(f"Помилка: {error}")


if __name__ == "__main__":
    main()