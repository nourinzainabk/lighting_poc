from roboflow import Roboflow
from app.core.config import settings

rf = Roboflow(api_key=settings.ROBOFLOW_API_KEY)

project = rf.workspace("lightning-ai").project("image-classification-vhs2u")
model = project.version(1).model

def predict_fixture(image_path: str):
    result = model.predict(image_path).json()
    return result["predictions"][0]
