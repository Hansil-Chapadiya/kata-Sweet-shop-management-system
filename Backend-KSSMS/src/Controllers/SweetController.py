#standard library imports
from fastapi import HTTPException, Body, BackgroundTasks
from fastapi.responses import JSONResponse
from datetime import datetime
from motor.motor_asyncio import AsyncIOMotorDatabase

#local imports
from config import params
from ..db.db_init import get_database
from ..Models.Sweet import SweetBase
from response_error import ErrorResponseModel

#third-party imports
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart


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
            background_tasks.add_task(
                cls.send_admin_notification, sweet_data.name, sweet_data.category
            )

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
