from pydantic import (
    BaseModel,
)  # Import BaseModel from Pydantic for data validation and serialization
from typing import List  # Import List for type hinting a list of items


class SweetItem(BaseModel):
    """
    Pydantic model representing a single sweet item within a purchase request.
    It specifies the sweet's unique identifier and the quantity to be purchased.
    """

    sweet_id: str  # The unique identifier (ID) of the sweet.
    quantity: int  # The     quantity of this specific sweet item to be purchased.


class PurchaseSweetRequest(BaseModel):
    """
    Pydantic model for a sweet purchase request.
    It contains a list of 'SweetItem' instances, representing multiple different sweets
    that a user wishes to purchase in a single transaction.
    """

    items: List[
        SweetItem
    ]  # A list of SweetItem objects, each detailing a sweet and its quantity.
