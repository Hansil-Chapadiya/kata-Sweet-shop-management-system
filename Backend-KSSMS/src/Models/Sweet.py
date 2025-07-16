# Standard library imports
from datetime import datetime, timezone
from enum import Enum
from typing import Optional

# Third-party library imports
from bson import ObjectId  # Used for MongoDB's unique document identifiers
from pydantic import (
    BaseModel,
    Field,
    HttpUrl,
)  # Pydantic for data validation and settings management

# Local application imports
# Assuming PyObjectId is a custom Pydantic type for handling ObjectId from MongoDB
from .ObjectIDValidator import PyObjectId


# Define the SweetCategory Enum
# This Enum provides a predefined set of categories for sweets, ensuring data consistency
class SweetCategory(str, Enum):
    """
    Enum for defining the allowed categories of sweets in the shop.
    Using an Enum helps standardize category names and prevents typos.
    """

    CHOCOLATE = "Chocolate"
    CANDY = "Candy"
    CAKE = "Cake"
    PASTRY = "Pastry"
    NUT_BASED = "Nut-based"
    MILK_BASED = "Milk-based"
    DRY_FRUIT = "Dry Fruit"
    FRUIT_BASED = "Fruit-based"
    SUGAR_FREE = "Sugar-free"


# Define the Sweet model for request/response payloads
# This model represents the structure of a sweet, used for data validation
# when adding or updating sweet information via the API.
class SweetBase(BaseModel):
    """
    Pydantic model representing a Sweet in the Sweet Shop Management System.
    This model is used for validating incoming request data and outgoing response data.
    """

    name: str = Field(
        ...,  # Ellipsis indicates this field is required
        min_length=1,
        max_length=50,
        description="The name of the sweet. Must be between 1 and 50 characters.",
    )
    category: SweetCategory = Field(
        ...,
        description="The category of the sweet, chosen from predefined SweetCategory enums.",
    )
    price: float = Field(
        ...,
        gt=0,  # price must be greater than 0
        description="The price of the sweet. Must be a positive floating-point number.",
    )
    quantity: int = Field(
        ...,
        ge=0,  # quantity must be greater than or equal to 0
        description="The quantity of the sweet currently in stock. Cannot be negative.",
    )
    discount: Optional[float] = Field(
        0,  # Default value if not provided
        ge=0,  # discount must be greater than or equal to 0
        le=100,  # discount must be less than or equal to 100
        description="Optional discount percentage for the sweet (0-100). Defaults to 0.",
    )
    description: Optional[str] = Field(
        None,  # Default value if not provided
        max_length=200,
        description="Optional brief description of the sweet, up to 200 characters.",
    )
    image_url: Optional[HttpUrl] = Field(
        None,  # Default value if not provided
        description="Optional URL pointing to an image of the sweet.",
    )

    @property
    def is_available(self) -> bool:
        """
        Calculates if the sweet is currently available based on its quantity in stock.

        Returns:
            bool: True if quantity is greater than 0, False otherwise.
        """
        return self.quantity > 0

    @property
    def final_price(self) -> float:
        """
        Calculates the final price of the sweet after applying any discount.

        Returns:
            float: The final price, rounded to two decimal places.
        """
        # Ensure discount defaults to 0 if None to avoid errors in calculation
        discount_value = self.discount or 0
        return round(self.price * (1 - discount_value / 100), 2)


# Define the SweetInDB model for database representation
# This model extends the Sweet model by adding database-specific fields
# like a unique ID and timestamps for creation and last update.
class SweetInDB(SweetBase):
    """
    Pydantic model representing a Sweet as stored in the database.
    Extends the `Sweet` model with database-specific fields like `_id`, `created_at`, and `updated_at`.
    """

    id: PyObjectId = Field(
        default_factory=PyObjectId,
        alias="_id",  # Maps the `id` field to `_id` in MongoDB documents
        description="The unique identifier of the sweet in the database. Automatically generated.",
    )
    created_at: Optional[datetime] = Field(
        default_factory=lambda: datetime.now(timezone.utc),
        description="Timestamp when the sweet was created.",
    )
    updated_at: Optional[datetime] = Field(
        default_factory=lambda: datetime.now(timezone.utc),
        description="Timestamp of the last update.",
    )

    class Config:
        """
        Pydantic configuration class for SweetInDB model.
        Configures how the model interacts with data, especially for database operations.
        """

        allow_population_by_field_name = True
        # Allows Pydantic to populate fields using their `alias` (e.g., `_id` from MongoDB).

        arbitrary_types_allowed = True
        # Allows Pydantic models to contain fields of types not explicitly supported
        # by Pydantic's core (e.g., `ObjectId` from `bson` in this case).
        # This is necessary because PyObjectId is a custom type.

        json_encoders = {ObjectId: str}
        # Defines custom JSON encoders for specific types.
        # Here, it tells Pydantic to convert `ObjectId` instances into their string representation
        # when serializing the model to JSON, which is crucial for FastAPI's JSON responses.
