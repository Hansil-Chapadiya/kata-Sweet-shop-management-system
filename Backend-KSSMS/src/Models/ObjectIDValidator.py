from bson import ObjectId


# Custom validator for Pydantic to handle MongoDB's ObjectId
class PyObjectId(ObjectId):
    """
    Custom Pydantic type to handle MongoDB's ObjectId.

    This class extends `bson.ObjectId` and provides validation logic
    for Pydantic models, allowing `ObjectId` to be used directly
    as a field type in Pydantic models. It ensures that incoming
    values are valid `ObjectId` strings and serializes them correctly.
    """

    @classmethod
    def __get_validators__(cls):
        """
        Yields validator methods for Pydantic.
        Pydantic uses these methods to validate data when a model is created.
        """
        yield cls.validate

    @classmethod
    def validate(cls, v):
        """
        Validates the input value as a valid MongoDB ObjectId.

        Args:
            v: The value to validate. Can be a string, ObjectId, etc.

        Returns:
            ObjectId: The validated ObjectId instance.

        Raises:
            ValueError: If the input value is not a valid ObjectId.
        """
        if not ObjectId.is_valid(v):
            raise ValueError("Invalid ObjectId")
        return ObjectId(v)

    @classmethod
    def __modify_schema__(cls, field_schema):
        """
        Modifies the OpenAPI (JSON Schema) schema for this type.
        This ensures that tools like Swagger UI correctly display `ObjectId` fields as strings.
        """
        field_schema.update(type="string")
