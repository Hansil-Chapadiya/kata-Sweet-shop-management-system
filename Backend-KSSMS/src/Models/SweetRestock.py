from pydantic import BaseModel  # Import BaseModel from Pydantic for data validation and serialization


class RestockSweetRequest(BaseModel):
    """
    Pydantic model for a sweet restock request.
    Defines the expected structure of the data when a user requests to restock a sweet.
    """
    sweet_id: str  # The unique identifier of the sweet to be restocked.
    quantity: int  # The amount by which to increase the sweet's stock.