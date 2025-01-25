from typing import List

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from common import UserAlert
from common.schemas.user_alert import UserAlertCreate, UserAlertResponse

from ..database import get_db

router = APIRouter()


@router.post("/alerts/", response_model=UserAlertResponse)
def create_alert(alert: UserAlertCreate, db: Session = Depends(get_db)):
    db_alert = UserAlert(**alert.dict())
    db.add(db_alert)
    db.commit()
    db.refresh(db_alert)
    return db_alert


@router.get("/alerts/", response_model=List[UserAlertResponse])
def get_alerts(db: Session = Depends(get_db)):
    return db.query(UserAlert).all()


@router.get("/alerts/{alert_id}", response_model=UserAlertResponse)
def get_alert(alert_id: int, db: Session = Depends(get_db)):
    db_alert = db.query(UserAlert).filter(UserAlert.id == alert_id).first()
    if db_alert is None:
        raise HTTPException(status_code=404, detail="Alert not found")
    return db_alert


@router.put("/alerts/{alert_id}", response_model=UserAlertResponse)
def update_alert(alert_id: int, alert: UserAlertCreate, db: Session = Depends(get_db)):
    db_alert = db.query(UserAlert).filter(UserAlert.id == alert_id).first()
    if db_alert is None:
        raise HTTPException(status_code=404, detail="Alert not found")
    for key, value in alert.dict().items():
        setattr(db_alert, key, value)
    db.commit()
    db.refresh(db_alert)
    return db_alert


@router.delete("/alerts/{alert_id}", response_model=UserAlertResponse)
def delete_alert(alert_id: int, db: Session = Depends(get_db)):
    db_alert = db.query(UserAlert).filter(UserAlert.id == alert_id).first()
    if db_alert is None:
        raise HTTPException(status_code=404, detail="Alert not found")
    db.delete(db_alert)
    db.commit()
    return db_alert
