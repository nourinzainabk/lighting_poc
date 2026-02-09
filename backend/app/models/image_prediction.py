from sqlalchemy import Column, Integer, String, Float, ForeignKey
from sqlalchemy.orm import relationship
from app.database import Base

class ImagePrediction(Base):
    __tablename__ = "image_predictions"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)

    filename_original = Column(String, nullable=False)
    user_provided_class = Column(String, nullable=False)

    prediction_result = Column(String, nullable=False)
    confidence_score = Column(Float, nullable=False)

    user = relationship("User", back_populates="predictions")
