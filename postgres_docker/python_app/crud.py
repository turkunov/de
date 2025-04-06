from sqlalchemy.orm import Session
from python_app import models, schemas
from python_app.db import commit_on_success
from python_app.utils.dummy_generator import gen_metadata, gen_image
import uuid


def get_users(db: Session):
    return db.query(models.User).all()

@commit_on_success
def insert_random_user(db: Session, clear_cache: bool = False):
    random_person = gen_metadata()
    random_person['img'] = gen_image(random_person['gender'])
    random_person['id'] = str(uuid.uuid4())
    new_user = models.User(**random_person)
    if clear_cache:
        db.delete(models.User)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return random_person