import pytest

from app.agent import (
    CARTS,
    DISCOUNT_CODES,
    LOYALTY_POINTS,
    PROCESSED_ORDERS,
    award_loyalty_points,
    process_cart_checkout,
)


@pytest.fixture(autouse=True)
def reset_state():
    # Reset in-memory state before each test
    CARTS.clear()
    CARTS.update(
        {
            "cart1": {"user_id": "user123", "total": 100.0, "is_checked_out": False},
            "cart2": {"user_id": "user456", "total": 200.0, "is_checked_out": False},
            "cart3": {
                "user_id": "student_user",
                "total": 50.0,
                "is_checked_out": False,
            },
        }
    )

    DISCOUNT_CODES.clear()
    DISCOUNT_CODES.update(
        {
            "WELCOME50": False,
            "SUMMER20": False,
        }
    )

    LOYALTY_POINTS.clear()
    LOYALTY_POINTS.update(
        {
            "user123": 0,
            "user456": 0,
            "student_user": 0,
        }
    )

    PROCESSED_ORDERS.clear()


def test_successful_checkout_no_discount():
    result = process_cart_checkout(cart_id="cart1", user_id="user123")
    assert "Checkout success" in result
    assert "Original Total: $100.00" in result
    assert "Discount Applied: $0.00" in result
    assert "Final Total Charged: $100.00" in result
    assert CARTS["cart1"]["is_checked_out"] is True


def test_successful_checkout_with_discount():
    result = process_cart_checkout(
        cart_id="cart1", user_id="user123", discount_code="WELCOME50"
    )
    assert "Checkout success" in result
    assert "Original Total: $100.00" in result
    assert "Discount Applied: $50.00" in result
    assert "Final Total Charged: $50.00" in result
    assert CARTS["cart1"]["is_checked_out"] is True
    assert DISCOUNT_CODES["WELCOME50"] is True


def test_checkout_unregistered_user():
    result = process_cart_checkout(cart_id="cart1", user_id="unknown_user")
    assert "Checkout failed" in result
    assert "is not a registered user" in result


def test_checkout_nonexistent_cart():
    result = process_cart_checkout(cart_id="cart999", user_id="user123")
    assert "Checkout failed" in result
    assert "does not exist" in result


def test_checkout_ownership_mismatch():
    result = process_cart_checkout(cart_id="cart2", user_id="user123")
    assert "Checkout failed" in result
    assert "does not belong to user" in result


def test_checkout_double_checkout():
    # First checkout
    result = process_cart_checkout(cart_id="cart1", user_id="user123")
    assert "Checkout success" in result

    # Second checkout
    result2 = process_cart_checkout(cart_id="cart1", user_id="user123")
    assert "Checkout failed" in result2
    assert "has already been checked out" in result2


def test_checkout_invalid_discount():
    result = process_cart_checkout(
        cart_id="cart1", user_id="user123", discount_code="INVALID_CODE"
    )
    assert "Checkout failed" in result
    assert "Invalid discount code" in result


def test_checkout_already_redeemed_discount():
    DISCOUNT_CODES["WELCOME50"] = True
    result = process_cart_checkout(
        cart_id="cart1", user_id="user123", discount_code="WELCOME50"
    )
    assert "Checkout failed" in result
    assert "already been redeemed" in result


def test_award_loyalty_points_success():
    result = award_loyalty_points(user_id="user123", points=10, order_id="ORD-12345")
    assert "Success" in result
    assert LOYALTY_POINTS["user123"] == 10
    assert "ORD-12345" in PROCESSED_ORDERS


def test_award_loyalty_points_unregistered_user():
    result = award_loyalty_points(
        user_id="unknown_user", points=10, order_id="ORD-12345"
    )
    assert "Error" in result
    assert "is not a registered user" in result


def test_award_loyalty_points_non_positive():
    result = award_loyalty_points(user_id="user123", points=0, order_id="ORD-12345")
    assert "Error" in result
    assert "must be a positive integer" in result


def test_award_loyalty_points_empty_order_id():
    result = award_loyalty_points(user_id="user123", points=10, order_id="  ")
    assert "Error" in result
    assert "Order ID cannot be empty" in result


def test_award_loyalty_points_replay():
    result = award_loyalty_points(user_id="user123", points=10, order_id="ORD-12345")
    assert "Success" in result

    result2 = award_loyalty_points(user_id="user123", points=5, order_id="ORD-12345")
    assert "Error" in result2
    assert "has already been processed" in result2
    assert LOYALTY_POINTS["user123"] == 10  # Point balance remains same
