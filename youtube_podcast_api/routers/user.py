from fastapi import Depends
from sqlalchemy.orm import Session

from youtube_podcast_api.database import get_db
from fastapi import APIRouter, HTTPException
from youtube_podcast_api.controllers.user import AlreadyThereException, UserController as UC
from youtube_podcast_api.schemas.user import UserLogin, UserToken

router = APIRouter()


@router.put("/user/", response_model=UserToken)
async def create_user(userLogin: UserLogin, db: Session = Depends(get_db)):
    try:
        user = UC(db).create_user(user=userLogin)
    except AlreadyThereException:
        raise HTTPException(status_code=409, detail="User already registered")
    except Exception as e:  # NOQA
        raise HTTPException(status_code=500, detail="Could not create the user")
    return UserToken.construct(token=user.token)
