from fastapi import APIRouter
from backend.schemas.customer import HealthResponse
from backend.config import settings

router = APIRouter(tags=["Health"])

@router.get("/health", response_model=HealthResponse)
async def health_check():
    return HealthResponse(
        status="ok",
        database=True,
        model=True,
        model_version=settings.MODEL_VERSION
    )
