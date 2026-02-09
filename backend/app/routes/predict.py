from fastapi import APIRouter, UploadFile, File, Form, Depends
from sqlalchemy.orm import Session

from app.services.roboflow_service import predict_fixture
from app.utils.image_utils import save_temp_image
from app.database import get_db
from app.models.image_prediction import ImagePrediction
from app.models.user import User
from app.core.auth import get_current_user

PLACEMENT_MAP = {
    "path_light": "This fixture is best suited for pathways and driveways in residential landscape designs.",
    "spot_light": "Ideal for highlighting focal points such as trees and architectural features.",
    "wallwash_light": "Designed to evenly illuminate walls and large vertical surfaces.",
    "deck_lighting": "Perfect for enhancing visibility on decks, stairs, and railings."
}

router = APIRouter(prefix="/predict", tags=["prediction"])

@router.post("/")
def predict(
    file: UploadFile = File(...),
    user_provided_class: str = Form(...),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    
    image_path = save_temp_image(file.file.read())

    
    prediction = predict_fixture(image_path)
    fixture_class = prediction["top"]
    confidence = prediction["confidence"] * 100

    record = ImagePrediction(
        user_id=current_user.id,
        filename_original=file.filename,
        user_provided_class=user_provided_class,
        prediction_result=fixture_class,
        confidence_score=confidence
    )

    db.add(record)
    db.commit()
    db.refresh(record)

    return {
        "status": "success",
        "class": fixture_class,
        "confidence": confidence,
        "recommended_placement": PLACEMENT_MAP.get(
            fixture_class,
            "No recommendation available"
        )
    }
