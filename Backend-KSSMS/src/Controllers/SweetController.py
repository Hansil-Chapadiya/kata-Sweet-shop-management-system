from fastapi import HTTPException, Body, BackgroundTasks
from fastapi.responses import JSONResponse
from datetime import datetime, timedelta
from motor.motor_asyncio import AsyncIOMotorDatabase
from config import params
from ..db.db_init import get_database
from ..Models.Sweet import SweetBase, SweetCategory
from response_error import ErrorResponseModel
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart


class SweetController:
    @classmethod
    async def get_collection(cls) -> AsyncIOMotorDatabase:  # type: ignore
        database = await get_database()
        return database

    @classmethod
    async def create_sweet(
        cls, sweet_data: SweetBase, background_tasks: BackgroundTasks
    ) -> JSONResponse:
        try:
            collection = await cls.get_collection()
            sweets = collection["Sweets"]

            # Check if the sweet name already exists
            existing_sweet = await sweets.find_one({"name": sweet_data.name})
            if existing_sweet:
                raise HTTPException(
                    status_code=400,
                    detail={
                        "status": False,
                        "detail": "Sweet with this name already exists",
                    },
                )

            # Create a new sweet
            sweet_dict = sweet_data.dict()
            sweet_dict["created_at"] = datetime.utcnow().isoformat()
            sweet_dict["updated_at"] = sweet_dict["created_at"]
            sweet_dict["is_available"] = sweet_dict["quantity"] > 0

            new_sweet = await sweets.insert_one(sweet_dict)

            # Send an admin notification email in the background
            background_tasks.add_task(
                cls.send_admin_notification, sweet_data.name, sweet_data.category
            )

            return JSONResponse(
                content={
                    "status": True,
                    "sweet_id": str(new_sweet.inserted_id),
                    "message": "Sweet added successfully",
                }
            )

        except HTTPException as e:
            print(f"Error creating sweet: {e.detail}")
            raise HTTPException(status_code=e.status_code, detail=e.detail)
        except Exception as e:
            print(f"Error creating sweet: {e}")
            error_response = ErrorResponseModel(status=False, detail=f"{e}")
            raise HTTPException(status_code=500, detail=dict(error_response))

    @staticmethod
    def send_admin_notification(sweet_name: str, sweet_category: str):
        """Send an email to the admin notifying about a new sweet addition."""
        admin_email = params["gmail"]  # Replace with your email
        sender_email = params["gmail"]  # Replace with your email
        sender_password = params["mail_password"]  # Replace with your password
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

        msg = MIMEMultipart()
        msg["From"] = sender_email
        msg["To"] = admin_email
        msg["Subject"] = subject
        msg.attach(MIMEText(body, "plain"))

        try:
            server = smtplib.SMTP(smtp_server, smtp_port)
            server.starttls()
            server.login(sender_email, sender_password)
            server.sendmail(sender_email, admin_email, msg.as_string())
            server.quit()
            print(f"Admin notification email sent to {admin_email}")
        except Exception as e:
            print(f"Failed to send admin notification email: {e}")
