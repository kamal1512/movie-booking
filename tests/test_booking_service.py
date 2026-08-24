import pytest

from app.services.booking_service import calculate_total_price

def test_calculate_total_price():
    result = calculate_total_price(seats=3, price_per_seat=250)

    assert result == 750

def test_single_seat():

    result = calculate_total_price(
        seats=1,
        price_per_seat=250
    )

    assert result == 250

def test_invalid_seats():

    with pytest.raises(ValueError):

        calculate_total_price(
            seats=0,
            price_per_seat=250
        )