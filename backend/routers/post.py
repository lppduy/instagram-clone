import random
import shutil
import string
from typing import List
from fastapi import APIRouter, Depends, File, UploadFile, status
from fastapi.exceptions import HTTPException
from sqlalchemy.orm import Session
from auth.oauth2 import get_current_user
from routers.schemas import PostBase, PostDisplay
from db.database import get_db
from db import db_post
from routers.schemas import UserAuth

router = APIRouter(
    prefix="/posts",
    tags=["posts"],
)

image_url_types = ["absolute","relative"]

@router.post("", response_model=PostDisplay, status_code=status.HTTP_201_CREATED)
def create_post(request: PostBase, 
                db: Session = Depends(get_db),
                current_user: UserAuth = Depends(get_current_user)
                ):
    if request.image_url_type not in image_url_types:
        raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, 
        detail="Parameter 'image_url_type' must be either 'absolute' or 'relative'")
    return db_post.create(db, request)

@router.get("/all", response_model=List[PostDisplay])
def posts(db: Session = Depends(get_db)):
    return db_post.get_all(db)

@router.post("/image")
def upload_image(image: UploadFile = File(...)):
    letter = string.ascii_letters
    ran_str = ''.join(random.choice(letter) for i in range(10))
    new = f"_{ran_str}."
    file_name = new.join(image.filename.rsplit(".",1))
    path = f"images/{file_name}"

    with open(path, "w+b") as buffer:
        shutil.copyfileobj(image.file, buffer)
    
    return {"filename": path}