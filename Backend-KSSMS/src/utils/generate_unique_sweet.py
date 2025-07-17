from bson import ObjectId  # Import ObjectId for generating unique IDs
# Helper function to generate unique sweet names
def generate_unique_name(base="TestSweet"):
    return f"{base}_{ObjectId()}"