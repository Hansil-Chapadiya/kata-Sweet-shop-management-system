from fastapi import APIRouter, HTTPException, status
from src.Models.Sweet import SweetBase
from typing import List

sweetRouter = APIRouter()

# TEMPORARY: In-memory DB substitute
sweet_db = []

@sweetRouter.post("/", status_code=status.HTTP_201_CREATED)
def add_sweet(sweet: SweetBase):
    # Optional: check if name already exists (simulate unique constraint)
    for item in sweet_db:
        if item.name == sweet.name:
            raise HTTPException(status_code=400, detail="Sweet already exists")

    sweet_db.append(sweet)
    return sweet
