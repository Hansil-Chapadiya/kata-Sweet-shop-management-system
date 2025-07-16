import pytest
from src.Models.Sweet import SweetBase, SweetCategory

def test_valid_sweet_model():
    sweet = SweetBase(
        name="Kaju Katli",
        category=SweetCategory.NUT_BASED,
        price=100.0,
        quantity=10,
        discount=20,
        description="Delicious sweet",
        image_url="https://upload.wikimedia.org/wikipedia/commons/a/ac/Kaju_katli_sweet.jpg"
    )
    assert sweet.name == "Kaju Katli"
    assert sweet.is_available is True
    assert sweet.final_price == 80.0

def test_missing_required_field_name():
    with pytest.raises(ValueError):
        SweetBase(
            name="",
            category=SweetCategory.CANDY,
            price=10.0,
            quantity=5
        )

def test_negative_price():
    with pytest.raises(ValueError):
        SweetBase(
            name="Bad Sweet",
            category=SweetCategory.CAKE,
            price=-10.0,
            quantity=5
        )

def test_invalid_discount_over_100():
    with pytest.raises(ValueError):
        SweetBase(
            name="Too Sweet",
            category=SweetCategory.CAKE,
            price=50.0,
            quantity=5,
            discount=110.0
        )

def test_is_available_false():
    sweet = SweetBase(
        name="Empty Sweet",
        category=SweetCategory.SUGAR_FREE,
        price=30.0,
        quantity=0
    )
    assert sweet.is_available is False


def test_invalid_category():
    with pytest.raises(ValueError):
        SweetBase(
            name="Test",
            category="INVALID_CATEGORY",  # Not in SweetCategory enum
            price=10.0,
            quantity=5
        )

def test_invalid_image_url():
    with pytest.raises(ValueError):
        SweetBase(
            name="Test",
            category=SweetCategory.CANDY,
            price=10.0,
            quantity=5,
            image_url="not_a_url"
        )

def test_max_length_name():
    long_name = "A" * 50  # Assuming max_length=50
    sweet = SweetBase(
        name=long_name,
        category=SweetCategory.CANDY,
        price=10.0,
        quantity=5
    )
    assert sweet.name == long_name