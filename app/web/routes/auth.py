from fastapi import APIRouter, HTTPException, Depends, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from fastapi.responses import Response
from jose import jwt
from jose.exceptions import ExpiredSignatureError, JWTClaimsError, JWTError

from app.settings import Settings
from app.web.schemas import Credentials
from app.web.dependencies import make_settings


router = APIRouter()
security = HTTPBearer()


def authenticate_user(credentials: Credentials):
    """Authenticate user.

    Args:
        credentials (schemas.Credentials): user credentials.

    Returns:
        int: user id.
        None: if user cannot be authenticated.
    """
    raise NotImplementedError()


def verify_token(
    credentials: HTTPAuthorizationCredentials = Depends(security),
    settings: Settings = Depends(make_settings)
) -> int:
    """
    Verify a JWT token and extract the user ID from its payload.

    Args:
        credentials (HTTPAuthorizationCredentials): The token to be verified.

    Returns:
        int: The user ID extracted from the token payload.

    Raises:
        HTTPException: If the token is invalid or cannot be decoded.
    """
    try:
        payload = jwt.decode(
            credentials.credentials,
            settings.secret_key,
            algorithms=[settings.algorithm]
        )
        user_id = payload['user_id']
        return user_id
    except (
        JWTError,
        ExpiredSignatureError,
        JWTClaimsError,
    ) as exc:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail='Invalid token',
            headers={'WWW-Authenticate': 'Bearer'}
        ) from exc


@router.post('/login')
async def login(
    response: Response,
    credentials: Credentials,
    settings: Settings = Depends(make_settings)
):
    user_id = authenticate_user(credentials)
    if user_id:
        access_token = jwt.encode(
            {
                'user_name': credentials.username,
                'user_id': user_id
            },
            settings.secret_key,
            algorithm=settings.algorithm
        )

        response.headers['Authorization'] = f'Bearer {access_token}'
    else:
        raise HTTPException(
            status_code=401, detail='Invalid username or password'
        )
