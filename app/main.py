from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, DeclarativeBase
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy import Table, Column, Integer, String, Float, Boolean, ForeignKey
from fastapi.staticfiles import StaticFiles
#from passlib.context import CryptContext
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
#from dotenv import load_dotenv
import os

#db
DATABASE_URL="postgresql://myuser:mypasswd@localhost:5515/mydatabase"
engine = create_engine(DATABASE_URL) #veri tabanına erişmek için gerekli
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)# Session factory oluştur

class Base(DeclarativeBase):
    pass #sqlalchemy'de böyle veri tabanına erişilen sınıf açılır

def init_db():
    Base.metadata.drop_all(engine)   # Veritabanını her başlangıcta siler burayada dikkat !!!!!!!!
    Base.metadata.create_all(bind=engine) # Veritabanını oluşturur


# Session dependency (FastAPI için)
def get_session_db() -> 'Generator[Session, None]':
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


#jinja html css jd renderir'i
templates = Jinja2Templates(directory="templates")


### SECRET KEY ###
origins = [
    "http://localhost",
    "http://localhost:8080",
    "http://localhost:3000",
    "http://localhost:8000",
]

app = FastAPI()

@app.on_event("startup")
def startup_event():
    init_db()

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


app.mount("/static", StaticFiles(directory="static"), name="static")



@app.get("/", response_class=HTMLResponse, name="login_page")
async def read_root(request: Request):
    context = {"request": request}
    return templates.TemplateResponse("sayfa1.html", context)

@app.get("/register", response_class = HTMLResponse, name="register_page")
async def register_page(request: Request):
    context = {"request": request}
    return templates.TemplateResponse(
        request = request,
        name="sayfa2.html",
        context = context
    )