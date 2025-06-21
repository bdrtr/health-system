from contextlib import redirect_stderr
import datetime
from email import contentmanager
from email.policy import default
from enum import Enum
from http.client import HTTPException
from multiprocessing import context
import os
from pydoc import Doc
import shutil
from fastapi import HTTPException, status
from fastapi import File, UploadFile
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
from ultralytics import YOLO
import cv2
from typing import Annotated

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
app.mount("/uploads", StaticFiles(directory="uploads"), name="uploads")


UPLOAD_DIR = 'uploads'
os.makedirs(UPLOAD_DIR, exist_ok=True)

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
    logs : Mapped[list[str]] = mapped_column(JSON, default=[])


class DeletedUsers(Base):
    __tablename__ = 'deleted_users'

    id : Mapped[int] = mapped_column(primary_key=True)
    username : Mapped[str] = mapped_column(index=True)
    role : Mapped[str] = mapped_column(default='Hasta')
    date : Mapped[str] = mapped_column(default=datetime.datetime.now())




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


def get_current_user(request: Request):
    user_id = request.session.get("user_id")
    if user_id is None:
        raise HTTPException(
            status_code=status.HTTP_303_SEE_OTHER,
            headers={"Location": "/"}
        )

    return user_id


@app.get("/", response_class=HTMLResponse, name="login_page")
async def _login_page(request: Request):
    context = {"request": request}
    request.session.clear()
    return templates.TemplateResponse("sayfa1.html", context)


@app.post("/", response_class=HTMLResponse, name="login_page")
async def login_page(
    request: Request,
    email : str = Form(...),
    password : str = Form(...),
    role : str = Form(...),
    session : Session = Depends(get_session_db),
):
    request.session.clear()
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
    context = {'request': request, 'message': 'kayıt başarılı'}
    return templates.TemplateResponse(
        name='sayfa2.html',
        context=context
    )

@app.post("/register", response_class = HTMLResponse)
async def register_page(
    request: Request,
    name : str = Form(),
    email :str = Form(...),
    passwd: str = Form(...),
    passwd2 : str = Form(...),
    role : str = Form(...),
    db: Session = Depends(get_session_db), #veri tabanı bağlantı nesnesi
):
    
    exist = db.query(UserModel).filter(UserModel.email == email).first() #eşleşme kontrol
    if exist:
        context = {'request': request, 'error': 'bu eposta kayıtlı'}
        return templates.TemplateResponse(name="sayfa2.html", context=context)
    
    _model : UserModel | DoctorModel | AdminModel = Roles[role].value
    
    if (passwd == passwd2):
        new_user = _model(
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


@app.get("/getAppointment", name="getAppointment", dependencies=[Depends(get_current_user)])
async def _getApp(
    request: Request,
    session : Session = Depends(get_session_db)
):  

    _user_id = request.session.get('user_id')
    appointments = session.query(Appointment).filter(Appointment.patient_id == _user_id).all()
    _docs = session.query(DoctorModel).all()
    
    context = {'request' : request, 'appointments' : appointments, 'docs' : _docs}
    return templates.TemplateResponse('sayfa4.html', context)

    
@app.post('/getAppointment', dependencies=[Depends(get_current_user)])
async def getApp(
    request: Request,
    session : Session = Depends(get_session_db),
    doctor_id = Form(default=None),
    date = Form(...),
    clock = Form(...),
):
    if doctor_id is None:
        return templates.TemplateResponse('sayfa4.html', context={'request':request, 'error': 'doktor seçmediniz'})
    
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


@app.get("/uploadImg", name="uploadImg", dependencies=[Depends(get_current_user)])
async def _uploadImg(
    request: Request,
    user_id  = Annotated[int, Depends(get_current_user)]
):
    context = {'request' : request}
    return templates.TemplateResponse("sayfa6.html", context)

@app.post("/uploadImg", name='uploadImg' , dependencies=[Depends(get_current_user)])
async def uploadImg(
    request: Request,
    session : Session = Depends(get_session_db),
    file : UploadFile = File(...),
    user_id  = Annotated[int, Depends(get_current_user)]
):
    file_location = f"{UPLOAD_DIR}/{file.filename}"
    with open(file_location, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    _user_id = request.session.get('user_id')

    _user = session.query(UserModel).filter(UserModel.id == _user_id).first()
    
    if _user.mri_results is None:
        _user.mri_results = []

    _user.mri_results = _user.mri_results + [file_location]
    session.commit()
    session.refresh(_user)

    context = {'request' : request, 'file_location' : file_location}
    return templates.TemplateResponse("sayfa6.html", context)


@app.get('/getProfile', name="getProfile")
async def _getProfile(
    request : Request,
    session : Session = Depends(get_session_db)
):
    
    _user_id = request.session.get('user_id')
    print(_user_id)

    _user = session.query(UserModel).filter(UserModel.id == _user_id).first()
    if _user :
        context = {'request' : request, 'user': _user, 'role' : 'Hasta'}
        return templates.TemplateResponse('sayfa10.html', context = context)
    
    _doctor = session.query(DoctorModel).filter(DoctorModel.id == _user_id).first()
    if _doctor :
        context = {'request' : request, 'user': _doctor, 'role' : 'Doktor'}
        return templates.TemplateResponse('sayfa10.html', context = context)
    
    _admin = session.query(AdminModel).filter(AdminModel.id == _user_id).first()
    if _admin :
        context = {'request' : request, 'user': _admin, 'role' : 'Admin'}
        return templates.TemplateResponse('sayfa10.html', context = context)


@app.post('/getProfile')
async def getProfile(
    request: Request,
    session : Session = Depends(get_session_db),
    file : UploadFile = File(...),

):
    
    _user_id = request.session.get('user_id')
    _user = session.query(UserModel).filter(UserModel.id == _user_id).first()

    file_location = f"{UPLOAD_DIR}/{file.filename}"
    with open(file_location, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    _user.profile_photo = file_location
    session.commit()
    session.refresh(_user)

    context = {'request' : request, 'user': _user, 'role' : 'Hasta'}
    return templates.TemplateResponse('sayfa10.html', context = context)


@app.get('/logout', name='logout')
async def logout(
    request: Request
):
    
    request.session.clear()
    return RedirectResponse(url='/')

@app.get('/docAppoint', name="docAppoint")
async def _doc_appoint(
    request: Request,
    session: Session = Depends(get_session_db),

):
    _doc_id = request.session.get('user_id')
    appointments = session.query(Appointment).filter_by(doctor_id=_doc_id).all()

    context = {'request' : request, 'appointments': appointments}
    return templates.TemplateResponse('sayfa6.html', context=context)


@app.get('/myPatients', name="myPatients")
async def _showPatients(
    request : Request,
    session: Session = Depends(get_session_db),
):
    _doc_id = request.session.get('user_id')
    appointments = session.query(Appointment).filter_by(doctor_id=_doc_id).all()
    patients = [appointment.patient for appointment in appointments]

    context = {'request': request, 'patients' : patients}
    return templates.TemplateResponse('sayfa7.html', context=context)


@app.get('/SeekPatient', name='SeekPatient')
async def _patientSeek(
    request: Request,
    session: Session = Depends(get_session_db)
):
    ...


@app.get('/seekReport', name='seekReport')
async def _seekRaport(
    request: Request,
    session: Session = Depends(get_session_db)
):
    _doc_id = request.session.get('user_id')
    reports = session.query(RaportModel).filter_by(doctor_id=_doc_id).all() #doktorun raporları
    patients = [report.patient for report in reports] #raporların sahibi hastalar

    context = {'request': request, 'reports' : reports, 'patients' : list(set(patients))}
    return templates.TemplateResponse('sayfa8.html', context=context)


@app.get('/runAnly', name='runAnly')
def _runAnly(
    request: Request,
    session: Session = Depends(get_session_db)
):
    _user_id = request.session.get('user_id')
    _user = session.query(UserModel).filter(UserModel.id == _user_id).first()
    _doctor_id=None
    if len(_user.appointments) > 0:
        _doctor_id =_user.appointments[0].doctor_id
    else:
        return templates.TemplateResponse('sayfa6.html', context={
            'request': request,
            'err' : 'rontgen gondermek için bir randevu oluşturmalısınız'
            })


    file_src = _user.mri_results[-1]
    file_name =  file_src.split('.')
    _result_file = file_name[0]+'T.'+file_name[1]

    model = YOLO("../best.pt")
    result = model.predict(
        source = file_src,
        save=False,
    )

    image = cv2.imread(file_src)

    r = result[0]

    label='Nothing'
    score=0

    for box in r.boxes:
        cls_id = int(box.cls[0])            # sınıf index'i
        label = r.names[cls_id]             # sınıf ismi
        conf = float(box.conf[0])          # güven skoru
        x1,y1,x2,y2 = map(int, box.xyxy[0])

        cv2.rectangle(image, (x1,y1), (x2,y2), (0,0,255), 2)

        score = str(conf*3) if conf < 0.3 else str(conf *1.5)
        cv2.putText(image, score, (x1,y1 - 10),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0,0,255), 1)
      
    cv2.imwrite(_result_file, image)
    _score = float(score)
    percent = int(_score * 100)

    new_report = RaportModel(
        doctor_id = _doctor_id,
        patient_id = _user_id,
        diagnosis = label,
        doc_advice = 'istirahat',
        treatment_plan = 'ayda 3 kez doktor kontorlu',
        score = percent,
        img = _result_file,
        state = stateRaport.detect.value,
    )

    session.add(new_report)
    session.commit()
    session.refresh(_user)

    context = {'request': request}

    return RedirectResponse(url='/getRaports', status_code=303)

    
@app.post('/updateDiagno/{report_id}', name="updateDiagno")
async def _updateDiagno(
    report_id :int ,
    request: Request,
    session: Session = Depends(get_session_db),
    diagnosis: str = Form(...),

):
    _report = session.query(RaportModel).filter(RaportModel.id == report_id).first()
    _report.diagnosis = diagnosis

    session.commit()
    session.refresh(_report)

    return RedirectResponse(url='/seekReport', status_code=303)



@app.get('/treatPlan/{user_id}/{report_id}', name='treatPlan')
async def _treatPlan(
    request: Request,
    user_id : int,
    report_id : int,
    session : Session = Depends(get_session_db)
):
    _user = session.query(UserModel).filter(UserModel.id == user_id).first()
    _report = session.query(RaportModel).filter(RaportModel.id == report_id).first()

    context = {'request' : request, 'user' : _user, 'report' : _report}
    return templates.TemplateResponse('sayfa9.html', context=context)


@app.post('/treatUpdate/{report_id}', name="treatUpdate")
async def _treatUpdate(
    report_id :int ,
    request: Request,
    session: Session = Depends(get_session_db),
    treatment_plan: str = Form(...),

):
    print(treatment_plan)
    _report = session.query(RaportModel).filter(RaportModel.id == report_id).first()
    _report.treatment_plan = treatment_plan

    session.commit()
    session.refresh(_report)

    return RedirectResponse(url='/seekReport', status_code=303)

@app.get('/userManagement', name='userManagement')
async def _userManagement(
    request: Request,
    session: Session = Depends(get_session_db)
):
    _users = session.query(UserModel).all()
    _doctors = session.query(DoctorModel).all()

    return templates.TemplateResponse("sayfa11.html", context={'request':request, 'users' : _users, 'doctors' : _doctors})

@app.get('/getLogs', name='getLogs')
async def _getLogs(
    request: Request,
    session: Session = Depends(get_session_db)
):
    
    context = {'request' : request}
    return templates.TemplateResponse("sayfa12.html", context=context)

@app.post('/{role}/delete/{id}', name="delete")
async def _delete(
    request: Request,
    id : int,
    role : str,
    session : Session = Depends(get_session_db)

):
    if role == 'doctor':
        _doctor = session.query(DoctorModel).filter(DoctorModel.id == id).first()
        session.delete(_doctor)
        _temp =  DeletedUsers(
            username = _doctor.username,
            role = 'Doktor',
        )
        session.add(_temp)
        session.commit()

    
    if role == 'user':
        _user = session.query(UserModel).filter(UserModel.id == id ).first()
        session.delete(_user)
        _temp =  DeletedUsers(
            username = _user.username,
            role = 'Hasta',
        )
        session.add(_temp)
        session.commit()

    return RedirectResponse(url="/userManagement", status_code=303)


@app.get('/deletedUsers', name='deletedUsers')
async def _deletedUsers(
    request:Request,
    session : Session = Depends(get_session_db)
):
    
    _users = session.query(DeletedUsers).all()
    context = {'request' : request, 'users' : _users}

    return templates.TemplateResponse('sayfa14.html', context=context)


@app.get('/addNewUser', name="addNewUserGet")
async def _addNewUserGet(request : Request):
    context = {'request' : request}
    return templates.TemplateResponse("sayfa13.html", context=context)

@app.post('/addNewUser', name='addNewUser')
async def _addNewUser(
    request: Request,
    username : str = Form(...),
    email : str = Form(...),
    role : str = Form(...),
    password : str = Form(...),
    db : Session = Depends(get_session_db)
):
    
    exist = db.query(UserModel).filter(UserModel.email == email).first() #eşleşme kontrol
    if exist:
        context = {'request': request, 'error': 'bu eposta kayıtlı'}
        return templates.TemplateResponse(name="sayfa2.html", context=context)
    
    _model : UserModel | DoctorModel | AdminModel = Roles[role].value
    
    new_user = _model(
        username = username,
        passwd = password,
        email = email,
    )

    db.add(new_user)
    db.commit()
    db.refresh(new_user)
        
    context = {'request' : request}
    return RedirectResponse(url='/userManagement', status_code=303)
