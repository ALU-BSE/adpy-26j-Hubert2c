# IshemaLink API 🇷🇼

IshemaLink is a logistics platform designed to digitize Rwanda’s courier ecosystem,
connecting rural farmers, urban hubs, and cross-border trade routes across the EAC.

This API powers shipment tracking, pricing, user verification, and notifications.

## Features
- Modular architecture with **Domestic** and **International** logic.
- Rwanda-compliant KYC validation (Phone & NID).
- Async shipment status notifications.
- Cached pricing tariffs for low-latency queries.
- Paginated shipment manifests for low-bandwidth devices.
- Hybrid Authentication (Session + JWT) with rate limiting.
- Field-level encryption for sensitive data.
- Role-based access control (RBAC) for secure operations.

## Installation & Setup

1. Clone the repository:
```bash
git clone <your-repo-url>
cd adpy-26j-Hubert2c



2.Create and activate a virtual environment:

python -m venv venv
# Windows
.\venv\Scripts\Activate.ps1
# macOS/Linux
source venv/bin/activate



3.Install dependencies:

pip install -r requirements.txt




4.Configure environment variables:

copy .env.example .env
# Edit .env for your settings



5.Apply database migrations:

python manage.py migrate



6.Run the development server:

python manage.py runserver


Visit http://127.0.0.1:8000/ to test.


Testing the API

Use the provided Postman collection: IshemaLink_Collection.json.

All requests use pre-filled environment variables: {{base_url}} and {{auth_token}}.

Check /api/status/ for system health.

Author

Munezero Hubert