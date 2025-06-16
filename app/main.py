import datetime
from email.policy import default
from enum import Enum
from starlette.middleware.sessions import SessionMiddleware
from sqlalchemy import create_engine, ForeignKey, Table, JSON, Column
from sqlalchemy.orm import sessionmaker, DeclarativeBase, relationship
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Mapped, mapped_column
from fastapi.staticfiles import StaticFiles
#from passlib.context import CryptContext
from fastapi.responses import HTMLResponse
from pydantic  import BaseModel
from fastapi.templating import Jinja2Templates
from fastapi import Form
from fastapi import Depends
from sqlalchemy.orm import Session
from fastapi.responses import RedirectResponse

#db
DATABASE_URL="postgresql://myuser:mypasswd@localhost:5515/mydatabase"
engine = create_engine(DATABASE_URL) #veri tabanına erişmek için gerekli
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)# Session factory oluştur

class Base(DeclarativeBase):
    pass #sqlalchemy'de böyle veri tabanına erişilen sınıf açılır

def init_db():
    #Base.metadata.drop_all(engine)   # Veritabanını her başlangıcta siler burayada dikkat !!!!!!!!
    Base.metadata.create_all(bind=engine) # Veritabanını oluşturur


# Session dependency c
def get_session_db():
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
    SessionMiddleware, #session var, jwt kullnılmadı
    secret_key="key_secret"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


app.mount("/static", StaticFiles(directory="static"), name="static")


#--------------------------------------------Models---------------------------------------


#----REALITONS-----
doctor_patient = Table(
    'doctor_patient',
    Base.metadata,
    Column('doctor_id', ForeignKey('doctors.id'), primary_key=True),
    Column('patient_id', ForeignKey('users.id'), primary_key=True),
)


#pydantic modelleri ve sqlalchmey modelleri birbirinden farklıdır ve kullanılmadan önce bir birilerine dönüştürülmeleri gerekir
class BaseUser(BaseModel):
    id: int | None
    username : str | None
    passwd : str | None #normalde passwd şifreli tutulmalıdır.

    class Config:
        from_attributes = True

class OutUser(BaseUser):
    email: str

class UserModel(Base):

    __tablename__ = 'users'

    id : Mapped[int] = mapped_column(primary_key=True)
    username : Mapped[str] = mapped_column(index=True)
    passwd : Mapped[str] = mapped_column(index=True)
    email : Mapped[str] = mapped_column(unique=True)
    mri_results : Mapped[list[str]] = mapped_column(JSON, nullable=True)
    phone: Mapped[list[int]] = mapped_column(JSON,nullable=True)
    profile_photo : Mapped[str] = mapped_column(nullable=True)
    
    appointments = relationship("Appointment", back_populates="patient")
    reports = relationship('RaportModel', back_populates='patient')

    doctors = relationship(
        'DoctorModel',
        secondary=doctor_patient,
        back_populates="patients" #bu doktor'daki patiens değişkenidir aynısı doktorda da var oda doctors'u işareet eder
    )

    ##### doktorlar hastalarına hastalarım sekmesinden erişebilmeli
    ##### randevular hastaların oluşturuduğu randevulardır
    ##### raporlar hastalardan gelen raporlardır.


#-----------------ENUM---------------------
class stateAppointment(Enum):
    suspend = 'Beklemede'
    active = 'Onaylandı'
    denied = 'Reddedildi'

class stateRaport(Enum):
    suspend = 'Bekliyor'
    detect = 'Tespit Edildi'
    clear = 'Hastalık Yok'


class Proficiency(Enum):
    internal_med = 'Dahiliye'
    gen_denistry = 'Genel Diş'
    gen_surgery = 'Genel Cerrahi'
    ent = 'KBB'
    cosmotic_surgery = 'Estetik Cerrahi'

#---------------------------------------------




class DoctorModel(Base):

    __tablename__ = 'doctors'

    id : Mapped[int] = mapped_column(primary_key=True)
    username : Mapped[str] = mapped_column(index=True)
    passwd : Mapped[str] = mapped_column(index=True)
    email : Mapped[str] = mapped_column(unique=True)
    profiency : Mapped[str] = mapped_column(default=Proficiency.cosmotic_surgery.value, nullable=True)
    patients = relationship(
        "UserModel", ## sınıf adı
        secondary=doctor_patient,
        back_populates = "doctors"
    )

    appointments = relationship("Appointment", back_populates="doctor")
    reports = relationship('RaportModel', back_populates='doctor')
    

class AdminModel(Base):

    __tablename__ = 'admins'

    id : Mapped[int] = mapped_column(primary_key=True)
    username : Mapped[str] = mapped_column(index=True)
    passwd : Mapped[str] = mapped_column(index=True)
    email : Mapped[str] = mapped_column(unique=True)
    logs : Mapped[list[str]] = mapped_column(JSON)







class Appointment(Base):

    __tablename__ = 'appointments'

    id : Mapped[int] = mapped_column(primary_key=True)

    doctor_id : Mapped[int] = mapped_column(ForeignKey('doctors.id'))
    patient_id : Mapped[int] = mapped_column(ForeignKey('users.id'))

    app_date_time : Mapped[str] = mapped_column(default=datetime.datetime.utcnow)
    state : Mapped[str] = mapped_column(default=stateAppointment.suspend.value)

    doctor = relationship('DoctorModel', back_populates = 'appointments')
    patient = relationship('UserModel', back_populates = 'appointments')


class RaportModel(Base):

    __tablename__ = 'reports'

    id : Mapped[int] = mapped_column(primary_key=True)

    doctor_id : Mapped[int] = mapped_column(ForeignKey('doctors.id'))
    patient_id : Mapped[int] = mapped_column(ForeignKey('users.id'))

    diagnosis : Mapped[str] = mapped_column()
    doc_advice : Mapped[str] = mapped_column()
    treatment_plan : Mapped[str] = mapped_column()

    score : Mapped[int] = mapped_column()
    img : Mapped[str] = mapped_column(nullable=True)
    state : Mapped[str] = mapped_column(default=stateRaport.suspend.value)

    doctor = relationship('DoctorModel', back_populates = 'reports')
    patient = relationship('UserModel', back_populates = 'reports')
    

#--------------------ENUMS------------------

class Roles(Enum):
    Doktor = DoctorModel
    Hasta = UserModel
    Admin = AdminModel


#--------------------------------------------Services-------------------------------------


#-----------------------------------------------API--------------------------------------


@app.get("/", response_class=HTMLResponse, name="login_page")
async def _login_page(request: Request):
    context = {"request": request}
    return templates.TemplateResponse("sayfa1.html", context)


@app.post("/", response_class=HTMLResponse, name="login_page")
async def login_page(
    request: Request,
    email : str = Form(...),
    password : str = Form(...),
    role : str = Form(...),
    session : Session = Depends(get_session_db),
):
    
    _model : UserModel | DoctorModel | AdminModel = Roles[role].value
    _user = session.query(_model).filter(_model.email == email).first()
    if _user and _user.passwd == password:
        request.session['user_id'] = _user.id #kullanıcı oturumu açtı
        context = {"request" : request, 'role' : role}
        return templates.TemplateResponse('sayfa3.html', context)
    

    context = {"request": request, 'error': 'giriş başarısız'}
    return templates.TemplateResponse("sayfa1.html", context)

@app.get("/register", response_class=HTMLResponse, name='register_page')
async def register_page_show(
    request: Request,
):
    return templates.TemplateResponse(
        name='sayfa2.html',
        request = request
    )

@app.post("/register", response_class = HTMLResponse)
async def register_page(
    request: Request,
    name : str = Form(),
    email :str = Form(...),
    passwd: str = Form(...),
    passwd2 : str = Form(...),
    db: Session = Depends(get_session_db), #veri tabanı bağlantı nesnesi
):
    
    exist = db.query(UserModel).filter(UserModel.email == email).first() #eşleşme kontrol
    if exist:
        context = {'request': request, 'error': 'bu eposta kayıtlı'}
        return templates.TemplateResponse(name="sayfa2.html", context=context)
    
    if (passwd == passwd2):
        new_user = UserModel(
            username = name,
            passwd = passwd,
            email = email,
        )

        db.add(new_user)
        db.commit()
        db.refresh(new_user)
        
        
    context = {"request": request, 'message': 'kayıt başarılı'}
    return templates.TemplateResponse(
        name="sayfa2.html",
        context = context
    )



@app.get('/show')
async def _show_users(
    db : Session = Depends(get_session_db)
) -> list[OutUser]:
    
    _users : list[OutUser] = db.query(UserModel).all()
    return _users



@app.get('/rolescreen', name='role_screen')
async def _role_screen(
    request: Request,

):
    return templates.TemplateResponse(
        request=request,
        name='sayfa3.html'
    )

@app.post('/rolescreen', name='role_screen')
async def role_screen(
    request: Request,
    role : str = Form(...),
    session: Session = Depends(get_session_db),
):
    
    _model = Roles[role].value
    print(request.session.get('user_id'))


@app.get("/getAppointment", name="getAppointment")
async def _getApp(
    request: Request,
    session : Session = Depends(get_session_db)
):  

    _user_id = request.session.get('user_id')
    appointments = session.query(Appointment).filter(Appointment.patient_id == _user_id).all()
    _docs = session.query(DoctorModel).all()
    
    context = {'request' : request, 'appointments' : appointments, 'docs' : _docs}
    return templates.TemplateResponse('sayfa4.html', context)

    
@app.post('/getAppointment')
async def getApp(
    request: Request,
    session : Session = Depends(get_session_db),
    doctor_id = Form(...),
    date = Form(...),
    clock = Form(...),
):
    _user_id = request.session.get('user_id')
    #_doctor = session.query(DoctorModel).filter(DoctorModel.id == doctor_id).first()
    new_appointment = Appointment(
        doctor_id = doctor_id,
        patient_id = _user_id,
        app_date_time = date +" "+ clock
    )

    session.add(new_appointment)
    session.commit()
    session.refresh(new_appointment)
    
    return RedirectResponse(url='/getAppointment', status_code=303)



@app.post('/addDoc')
async def addDoc(
    request: Request,
    username : str,
    email: str,
    password : str,
    profiency : Proficiency,
    session: Session = Depends(get_session_db),
):
    
    new_doctor = DoctorModel(
        username = username,
        email = email,
        passwd = password,
        profiency = profiency.value
    )
    session.add(new_doctor)
    session.commit()
    session.refresh(new_doctor)
    

@app.get('/showdoc')
async def show_users(
    db : Session = Depends(get_session_db)
):
    
    _doctors = db.query(DoctorModel).all()
    return _doctors


@app.get('/getRaports', name="getRaports")
async def get_raports(
    request: Request,
    session : Session = Depends(get_session_db)
):
    _id = request.session.get('user_id')
    _reports = session.query(RaportModel).filter(RaportModel.patient_id == _id).all()

    context = {'request' : request, 'reports' : _reports}
    return templates.TemplateResponse('sayfa5.html', context=context)