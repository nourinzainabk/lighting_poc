from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.routes.predict import router as predict_router
from app.routes.auth import router as auth_router
from app.database import Base, engine
from app.core.config import settings

import app.models.user
import app.models.image_prediction


app = FastAPI(title="Lighting Fixture Classifier")

Base.metadata.create_all(bind=engine)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


app.include_router(auth_router)
app.include_router(predict_router)
