from fastapi import FastAPI
from app.routes.predict import router as predict_router
from app.routes.auth import router as auth_router
from app.database import Base, engine

import app.models.user
import app.models.image_prediction  
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(title="Lighting Fixture Classifier")

Base.metadata.create_all(bind=engine)

app.include_router(auth_router)
app.include_router(predict_router)
origins = [
    "http://localhost:5173",  # React dev server
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)