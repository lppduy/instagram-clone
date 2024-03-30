from fastapi import FastAPI
from db import models
from db.database import engine
from routers.user import router as user_router
from routers.post import router as post_router
from auth.authentication import router as auth_router
from fastapi.staticfiles import StaticFiles

app = FastAPI()

app.include_router(user_router)
app.include_router(post_router)
app.include_router(auth_router)

@app.get("/")
def root():
    return {"message": "Hello World"}

models.Base.metadata.create_all(engine)

app.mount("/images", StaticFiles(directory="images"), name="images")