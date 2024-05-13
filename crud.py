from sqlalchemy.orm import Session
import requests
import models, schemas
from gibberish_detector import detector
from googletrans import Translator

def get_user(db: Session, id: int):
    return db.query(models.customer_request).filter(models.customer_request.id == id).first()

def get_user_by_name(db: Session, customer_name: str):
    return db.query(models.customer_request).filter(models.customer_request.customer_name == customer_name).first()

def get_users(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.customer_request).offset(skip).limit(limit).all()

def create_user(db: Session, user: schemas.UserCreate):
    db_user = models.customer_request(customer_name=user.customer_name, contact_email = user.contact_email,customer_input_date = user.customer_input_date,customer_input_address = user.customer_input_address, content = user.content, url = user.url)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

def pretext_handling(result):
    predictresult = "fake"
    if result>0.8:
        predictresult = "real"
    elif result>0.6:
        predictresult = "likely real"
    elif result>0.4:
        predictresult = "ambiguous"
    elif result>0.2:
        predictresult = "likely fake"
    return predictresult

def url_is_valid(url):
    if not url.startswith(('http://', 'https://')):
        url = 'https://' + url
    try:
        r = requests.get(url)
        if r.status_code == 200:
            return True
        else:
            return False
    except:
        return False

def text_is_Gibberish(text):
    Detector = detector.create_from_model('big.model')
    return Detector.is_gibberish(text)

def text_is_English(text):
    translator = Translator()
    return translator.detect(text).lang == "en"
