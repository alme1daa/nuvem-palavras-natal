from fastapi import APIRouter, Depends, HTTPException, Request
from sqlalchemy.orm import Session
from datetime import datetime, timedelta
from pydantic import BaseModel
from jose import jwt, JWTError
from app.database import get_db
from app.config import settings
from app.models import WordSubmission, WordAggregate, ConfigSetting, AllowedWord, BlockedWord
from app.moderation import normalize_text, validate_word_format

router = APIRouter()

class SubmissionSchema(BaseModel):
    word: str

class LoginSchema(BaseModel):
    username: str
    password: str

class WordActionSchema(BaseModel):
    submission_id: int

def verify_token(request: Request):
    auth_header = request.headers.get("Authorization")
    if not auth_header or not auth_header.startswith("Bearer "):
        raise HTTPException(status_code=401, detail="Não autorizado")
    try:
        return jwt.decode(auth_header.split(" ")[1], settings.JWT_SECRET, algorithms=["HS256"])
    except JWTError:
        raise HTTPException(status_code=401, detail="Sessão expirada")

@router.get("/config/public")
def get_public_config():
    return {"public_url": settings.PUBLIC_URL}

@router.get("/cloud/words")
def get_cloud_words(db: Session = Depends(get_db)):
    words = db.query(WordAggregate).order_by(WordAggregate.frequency.desc()).limit(100).all()
    total = db.query(WordSubmission).filter(WordSubmission.status == "approved").count()
    return {"words": [{"text": w.word, "value": w.frequency} for w in words], "total_approved": total}

@router.post("/submit")
def submit_word(data: SubmissionSchema, request: Request, db: Session = Depends(get_db)):
    ip = request.client.host if request.client else "127.0.0.1"
    valid, msg = validate_word_format(data.word)
    if not valid:
        raise HTTPException(status_code=400, detail=msg)

    raw_word = data.word.strip()
    norm_word = normalize_text(raw_word)

    sub = WordSubmission(raw_word=raw_word, normalized_word=norm_word, status="approved", ip_address=ip)
    db.add(sub)
    
    agg = db.query(WordAggregate).filter(WordAggregate.word == raw_word.capitalize()).first()
    if agg:
        agg.frequency += 1
    else:
        db.add(WordAggregate(word=raw_word.capitalize(), frequency=1))
        
    db.commit()
    return {"status": "success", "message": "Palavra publicada!"}

@router.post("/admin/login")
def admin_login(data: LoginSchema):
    if data.username == settings.ADMIN_USERNAME and data.password == settings.ADMIN_PASSWORD:
        return {"access_token": jwt.encode({"sub": data.username}, settings.JWT_SECRET, algorithm="HS256")}
    raise HTTPException(status_code=401, detail="Credenciais inválidas")