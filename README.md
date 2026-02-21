# IshemaLink API 🇷🇼

IshemaLink is a logistics platform designed to digitize Rwanda’s courier ecosystem,
connecting rural farmers, urban hubs, and cross-border trade routes across EAC.

This API powers shipment tracking, pricing, user verification, and notifications.

---

## Features
- Modular architecture separating Domestic & International logic
- Rwanda-compliant KYC validation (Phone & NID)
- Asynchronous shipment status notifications
- Cached pricing tariffs for performance
- Paginated shipment manifests for low-bandwidth devices

---

## Requirements
- Python 3.14+
- Django 6.0+
- Django REST Framework
- Redis (optional, for caching)
- Postman (for API testing)

---

## Quick Setup & Run Commands

**Windows (PowerShell)**:
```powershell
git clone <your-repo-url>
cd IshemaLink_api
python -m venv venv
.\venv\Scripts\Activate.ps1
pip install --upgrade pip
pip install -r requirements.txt
copy .env.example .env
python manage.py migrate
python manage.py createsuperuser  
python manage.py runserver

## for MACOS/Linux

git clone <your-repo-url>
cd IshemaLink_api
python3 -m venv venv
source venv/bin/activate
pip install --upgrade pip
pip install -r requirements.txt
cp .env.example .env
python manage.py migrate
python manage.py createsuperuser  # optional
python manage.py runserver



API available at: http://127.0.0.1:8000/

Health check: http://127.0.0.1:8000/api/status/



Testing the API

Import Postman Collection: IshemaLink_Collection.json

Import Environment: IshemaLink_Env.json

Set your auth_token in the environment after registering/logging in

Test key endpoints:






## Author

Munezero Hubert

