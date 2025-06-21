# HEALTH-SYSTEM

- Bu aracı geliştirmeye başlamak ve test ortamında sunmak için aşağıdaki yönergeleri takip et:

```bash

git clone https://github.com/bdrtr/health-system.git
cd health-system
```

- linux:
```
source myenv/bin/activate
```
- windows(powershell) cmd'de farklıdır:
```
myenv\Scripts\Activate.ps1
```
- bağımlılıkları yükle
```
pip install -r requirements.txt
```

- docker builder'ın çalıştığından emin ol!
```bash
docker compose up -d
```
- diğer portlarla çakışmadığından emin ol.

```bash
cd app
```
- Celery ile çalışmak için worker'ı başlat:

```bash
celery -A main.celery_app worker --loglevel=info
```
- bu terminal artık worker için ayrıldı yeni bir teminalde sanal ortam'a tekrar gir ve app klasörüne gel.

```
fastapi dev
```

sistemi ayağa kaldırdık.

- terminaldeki açılan linkte tıkla

## Tech Stack

**Front-end:** Html, CSS, jinja2(html renderer), Bootstrap

**Back-end:** Python FastApi

**Server:** Uvicorn

**Database:** PostgreSql

**ORM:** Sqlalchemy

**Caching:** Redis, Celery

**Classification:** YoloV8

