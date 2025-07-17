# standard library imports
from fastapi import HTTPException, Body, BackgroundTasks
from fastapi.responses import JSONResponse
from datetime import datetime
from motor.motor_asyncio import AsyncIOMotorDatabase

# local imports
from config import params
from ..db.db_init import get_database
from ..Models.Sweet import SweetBase
from response_error import ErrorResponseModel

# third-party imports
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from bson import ObjectId


class SweetController:
    """
    Controller class for managing sweet-related operations.
    Handles business logic and interacts with the database.
    """

    @classmethod
    async def get_collection(cls) -> AsyncIOMotorDatabase:  # type: ignore
        """
        Retrieves the MongoDB database instance.
        """
        database = await get_database()
        return database

    @classmethod
    async def get_sweets(cls) -> JSONResponse:
        """
        Retrieves all sweets from the database.
        Returns a JSON response with the list of sweets.
        """
        try:
            collection = await cls.get_collection()
            sweets = collection["Sweets"]
            sweet_list = []

            async for sweet in sweets.find():
                sweet["_id"] = str(sweet["_id"])  # Convert ObjectId to string
                sweet_list.append(sweet)

            return JSONResponse(
                content={
                    "status": True,
                    "sweets": sweet_list,
                    "message": "Sweets retrieved successfully",
                }
            )
        except Exception as e:
            print(f"Error retrieving sweets: {e}")
            error_response = ErrorResponseModel(status=False, detail=f"{e}")
            raise HTTPException(status_code=500, detail=dict(error_response))

    @classmethod
    async def get_sweet(cls, sweet_id: str) -> JSONResponse:
        """
        Retrieves a sweet by its ID from the database.
        Returns a JSON response with the sweet details.
        """
        try:
            collection = await cls.get_collection()
            sweets = collection["Sweets"]
            sweet = await sweets.find_one({"_id": ObjectId(sweet_id)})

            if not sweet:
                raise HTTPException(
                    status_code=404,
                    detail={"status": False, "detail": "Sweet not found"},
                )

            sweet["_id"] = str(sweet["_id"])  # Convert ObjectId to string
            return JSONResponse(
                content={
                    "status": True,
                    "sweet": sweet,
                    "message": "Sweet retrieved successfully",
                }
            )
        except HTTPException as e:
            raise e

    @classmethod
    async def delete_sweet(cls, sweet_id: str) -> JSONResponse:
        """
        Deletes a sweet by its ID from the database.
        Returns a JSON response indicating success or failure.
        """
        try:
            collection = await cls.get_collection()
            sweets = collection["Sweets"]

            # Validate the ObjectId format for MongoDB
            if not ObjectId.is_valid(sweet_id):
                raise HTTPException(
                    status_code=400,
                    detail={"status": False, "detail": "Invalid sweet ID format"},
                )

            # Attempt to delete the sweet
            result = await sweets.delete_one({"_id": ObjectId(sweet_id)})

            if result.deleted_count == 0:
                raise HTTPException(
                    status_code=404,
                    detail={"status": False, "detail": "Sweet not found"},
                )

            return JSONResponse(
                content={
                    "status": True,
                    "message": "Sweet deleted successfully",
                }
            )
        except HTTPException as e:
            raise e
        except Exception as e:
            print(f"Error deleting sweet: {e}")
            error_response = ErrorResponseModel(status=False, detail=f"{e}")
            raise HTTPException(status_code=500, detail=dict(error_response))

    @classmethod
    async def search_sweets(cls, search_query: str, sort_by: str = None, order: str = "asc") -> JSONResponse:  # type: ignore
        """
        Searches for sweets based on a query string.
        Supports searching by name, category, description, and price.
        Returns a JSON response with the list of matching sweets.
        """
        try:
            collection = await cls.get_collection()
            sweets = collection["Sweets"]
            sweet_list = []

            try:
                search_price = float(search_query)
            except ValueError:
                search_price = None

            query = {
                "$or": [
                    {"name": {"$regex": search_query, "$options": "i"}},
                    {"category": {"$regex": search_query, "$options": "i"}},
                    {"description": {"$regex": search_query, "$options": "i"}},
                ]
            }

            if search_price is not None:
                query["$or"].append({"price": search_price})  # type: ignore

            # Build sort tuple
            sort_field = sort_by if sort_by in ["price", "name"] else None
            sort_order = -1 if order == "desc" else 1

            cursor = sweets.find(query)
            if sort_field:
                cursor = cursor.sort(sort_field, sort_order)

            cursor = cursor.limit(15)

            async for sweet in cursor:
                sweet["_id"] = str(sweet["_id"])
                sweet_list.append(sweet)

            # Fallback for price search
            if not sweet_list and search_price is not None:
                fallback_cursor = sweets.find({"price": {"$gt": search_price}})
                if sort_field:
                    fallback_cursor = fallback_cursor.sort(sort_field, sort_order)
                fallback_cursor = fallback_cursor.limit(15)

                async for sweet in fallback_cursor:
                    sweet["_id"] = str(sweet["_id"])
                    sweet_list.append(sweet)

            return JSONResponse(
                content={
                    "status": True,
                    "sweets": sweet_list,
                    "message": "Sweets retrieved successfully",
                }
            )

        except Exception as e:
            print(f"Error searching sweets: {e}")
            error_response = ErrorResponseModel(status=False, detail=str(e))
            raise HTTPException(status_code=500, detail=error_response.dict())

    @classmethod
    async def purchase_sweet(cls, sweet_id: str, quantity: int) -> dict:
        """
        Processes the purchase of a sweet by its ID and quantity.
        Validates the quantity and updates the sweet's stock.
        Returns a dictionary with the purchase result.
        """
        try:
            if quantity <= 0:
                raise HTTPException(
                    status_code=400,
                    detail={
                        "status": False,
                        "message": "Quantity must be greater than zero",
                    },
                )
            collection = await cls.get_collection()
            sweets = collection["Sweets"]

            sweet = await sweets.find_one({"_id": ObjectId(sweet_id)})
            if not sweet:
                raise HTTPException(
                    status_code=404,
                    detail={"status": False, "message": "Sweet not found"},
                )

            if sweet["quantity"] < quantity:
                raise HTTPException(
                    status_code=400,
                    detail={
                        "status": False,
                        "message": "Not enough quantity available",
                    },
                )

            new_quantity = sweet["quantity"] - quantity
            await sweets.update_one(
                {"_id": ObjectId(sweet_id)}, {"$set": {"quantity": new_quantity}}
            )

            return {
                "status": True,
                "message": "Purchase successful",
                "remaining_quantity": new_quantity,
            }
        except HTTPException as e:
            raise HTTPException(status_code=e.status_code, detail=e.detail)
        except Exception as e:
            print(f"Error searching sweets: {e}")
            error_response = ErrorResponseModel(status=False, detail=str(e))
            raise HTTPException(
                status_code=500,
                detail={"status": False, "message": error_response.dict()},
            )

    @classmethod
    async def restock_sweet(cls, sweet_id: str, quantity: int) -> JSONResponse:
        """
        Restocks a sweet by its ID and quantity.
        Validates the quantity and updates the sweet's stock.
        Returns a JSON response with the restock result.
        """
        try:
            if quantity <= 0:
                raise HTTPException(
                    status_code=400,
                    detail={
                        "status": False,
                        "message": "Quantity must be greater than zero",
                    },
                )
            collection = await cls.get_collection()
            sweets = collection["Sweets"]

            sweet = await sweets.find_one({"_id": ObjectId(sweet_id)})
            if not sweet:
                raise HTTPException(
                    status_code=404,
                    detail={"status": False, "message": "Sweet not found"},
                )

            new_quantity = sweet["quantity"] + quantity
            await sweets.update_one(
                {"_id": ObjectId(sweet_id)}, {"$set": {"quantity": new_quantity}}
            )

            return JSONResponse(
                content={
                    "status": True,
                    "message": "Restock successful",
                    "updated_stock": new_quantity,
                }
            )
        except HTTPException as e:
            raise HTTPException(status_code=e.status_code, detail=e.detail)
        except Exception as e:
            raise HTTPException(
                status_code=500, detail={"status": False, "message": str(e)}
            )

    @classmethod
    async def create_sweet(
        cls, sweet_data: SweetBase, background_tasks: BackgroundTasks
    ) -> JSONResponse:
        """
        Creates a new sweet entry in the database.
        Checks for existing sweet names and sends an admin notification.
        """
        try:
            collection = await cls.get_collection()
            sweets = collection["Sweets"]

            # Check if the sweet name already exists to prevent duplicates
            existing_sweet = await sweets.find_one({"name": sweet_data.name})
            if existing_sweet:
                raise HTTPException(
                    status_code=400,
                    detail={
                        "status": False,
                        "detail": "Sweet with this name already exists",
                    },
                )

            # Prepare sweet data for insertion, adding timestamps and availability status
            sweet_dict = sweet_data.dict()
            sweet_dict["created_at"] = datetime.utcnow().isoformat()
            sweet_dict["updated_at"] = sweet_dict["created_at"]
            sweet_dict["is_available"] = sweet_dict["quantity"] > 0

            # Insert the new sweet into the database
            new_sweet = await sweets.insert_one(sweet_dict)

            # Send an admin notification email in the background to avoid blocking the response
            # background_tasks.add_task(
            #     cls.send_admin_notification, sweet_data.name, sweet_data.category
            # )

            # Return a success JSON response with the ID of the newly created sweet
            return JSONResponse(
                content={
                    "status": True,
                    "sweet_id": str(new_sweet.inserted_id),
                    "message": "Sweet added successfully",
                }
            )

        except HTTPException as e:
            # Re-raise HTTPException directly for FastAPI to handle
            print(f"Error creating sweet: {e.detail}")
            raise HTTPException(status_code=e.status_code, detail=e.detail)
        except Exception as e:
            # Catch any other unexpected errors and return a 500 Internal Server Error
            print(f"Error creating sweet: {e}")
            error_response = ErrorResponseModel(status=False, detail=f"{e}")
            raise HTTPException(status_code=500, detail=dict(error_response))

    @staticmethod
    def send_admin_notification(sweet_name: str, sweet_category: str):
        """
        Sends an email to the admin notifying about a new sweet addition.
        This runs as a background task.
        """
        admin_email = params["gmail"]  # Admin's email address from config
        sender_email = params["gmail"]  # Sender's email address from config
        sender_password = params["mail_password"]  # Sender's email password from config
        smtp_server = "smtp.gmail.com"
        smtp_port = 587

        subject = "New Sweet Added to Inventory"
        body = f"""
        Admin,

        A new sweet has been added to the inventory.

        Name: {sweet_name}
        Category: {sweet_category}

        Please review the sweet details.

        Regards,
        Sweet Shop Management System
        """

        # Create the email message
        msg = MIMEMultipart()
        msg["From"] = sender_email
        msg["To"] = admin_email
        msg["Subject"] = subject
        msg.attach(MIMEText(body, "plain"))

        try:
            # Establish SMTP connection and send the email
            server = smtplib.SMTP(smtp_server, smtp_port)
            server.starttls()  # Upgrade connection to secure TLS
            server.login(sender_email, sender_password)
            server.sendmail(sender_email, admin_email, msg.as_string())
            server.quit()
            print(f"Admin notification email sent to {admin_email}")
        except Exception as e:
            # Log any errors encountered during email sending
            print(f"Failed to send admin notification email: {e}")
