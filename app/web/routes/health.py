from fastapi import APIRouter

from app.web.schemas import HealthCheckResponse
from app.web.utils import check_database
from app.settings import Settings


router = APIRouter()
settings = Settings()

@router.get(
    '/health',
    summary='Check API health status',
    description=(
        'Returns a response indicating whether the API and Database are '
        'up and running.'
    )
)
async def health() -> HealthCheckResponse:
    """
    Check API health status.

    Returns:
        A dictionary with 'api' and 'database' keys with boolean values
        indicating whether they are up and running.
    """
    database_status = check_database(settings.db_url)

    return HealthCheckResponse(api=True, database=database_status)
