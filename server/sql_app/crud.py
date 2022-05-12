from sqlalchemy.orm import Session
from . import models, schemas

def get_pair(db: Session, pair_id: int):
    return db.query(models.Pair).filter(models.Pair.id == pair_id).first()

def create_pair(db: Session, pair: schemas.PairCreate, pair_id: int):
    db_pair = models.Pair(**pair.dict(), pair_id)
    db.add(db_pair)
    db.commit()
    db.refresh(db_pair)
    return db_pair