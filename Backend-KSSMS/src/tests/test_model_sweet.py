import pytest
from src.Models.Sweet import SweetBase, SweetCategory


#  Test that a valid sweet creates correctly and computed fields work
def test_valid_sweet_model():
    sweet = SweetBase(
        name="Kaju Katli",
        category=SweetCategory.NUT_BASED,
        price=100.0,
        quantity=10,
        discount=20,
        description="Delicious sweet",
        image_url="https://upload.wikimedia.org/wikipedia/commons/a/ac/Kaju_katli_sweet.jpg",
    )
    assert sweet.name == "Kaju Katli"
    assert sweet.is_available is True  # Computed field
    assert sweet.final_price == 80.0  # 100 - 20% discount


#  Test name field is required and cannot be empty
def test_missing_required_field_name():
    with pytest.raises(ValueError):  # Pydantic raises ValueError for validation
        SweetBase(name="", category=SweetCategory.CANDY, price=10.0, quantity=5)


#  Test price cannot be negative
def test_negative_price():
    with pytest.raises(ValueError):
        SweetBase(
            name="Bad Sweet", category=SweetCategory.CAKE, price=-10.0, quantity=5
        )


#  Test discount must be between 0 and 100
def test_invalid_discount_over_100():
    with pytest.raises(ValueError):
        SweetBase(
            name="Too Sweet",
            category=SweetCategory.CAKE,
            price=50.0,
            quantity=5,
            discount=110.0,
        )


#  Test is_available returns False when quantity is 0
def test_is_available_false():
    sweet = SweetBase(
        name="Empty Sweet", category=SweetCategory.SUGAR_FREE, price=30.0, quantity=0
    )
    assert sweet.is_available is False


#  Test that invalid enum value for category raises error
def test_invalid_category():
    with pytest.raises(ValueError):
        SweetBase(
            name="Test",
            category="INVALID_CATEGORY",  # Not in SweetCategory enum
            price=10.0,
            quantity=5,
        )


#  Test invalid image URL is caught
def test_invalid_image_url():
    with pytest.raises(ValueError):
        SweetBase(
            name="Test",
            category=SweetCategory.CANDY,
            price=10.0,
            quantity=5,
            image_url="not_a_url",  # Invalid URL
        )


#  Test max length of name field works (limit is 50)
def test_max_length_name():
    long_name = "A" * 50  # 50 characters = OK
    sweet = SweetBase(
        name=long_name, category=SweetCategory.CANDY, price=10.0, quantity=5
    )
    assert sweet.name == long_name
