from fastapi import APIRouter, Depends, Header
from fastapi.exceptions import HTTPException
from sqlalchemy.orm import Session

from youtube_podcast_api.database import get_db
from youtube_podcast_api.schemas.user import UserToken
from youtube_podcast_api.controllers.user import UserController as UC

router = APIRouter()


@router.get("/auth/", response_model=UserToken)
async def get_token(Bearer: str = Header(None), db: Session = Depends(get_db)):
    try:
        user = UC(db).get_user_from_id_token(Bearer)
        return UserToken.construct(token=user.token)
    except Exception:
        raise HTTPException(status_code=404, detail="Could not find this user in the db")
