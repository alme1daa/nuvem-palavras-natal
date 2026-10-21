from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from app.routes import router
from app.database import engine, Base

Base.metadata.create_all(bind=engine)

app = FastAPI(title="SENAI Wordcloud Natal")
app.add_middleware(CORSMiddleware, allow_origins=["*"], allow_credentials=True, allow_methods=["*"], allow_headers=["*"])
app.include_router(router, prefix="/api")
app.mount("/", StaticFiles(directory="public", html=True), name="public")
from datetime import datetime, timedelta

@app.get("/api/words")
def get_words(db: Session = Depends(get_db)):
    # Filtra apenas palavras enviadas nas últimas 6 horas
    limite_tempo = datetime.utcnow() - timedelta(hours=6)
    
    palavras = db.query(PalavraModel)\
                 .filter(PalavraModel.created_at >= limite_tempo)\
                 .all()
                 
    return palavras