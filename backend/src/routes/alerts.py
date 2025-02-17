from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from common import UserAlert
from common.database import get_db
from common.schemas.user_alert import UserAlertCreate, UserAlertResponse

router = APIRouter()


@router.post("/alerts/", response_model=UserAlertResponse)
def create_alert(alert: UserAlertCreate, db: Session = Depends(get_db)):
    db_alert = UserAlert(**alert.model_dump())
    db.add(db_alert)
    db.commit()
    db.refresh(db_alert)
    return db_alert
