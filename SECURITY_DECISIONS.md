# Security Decisions for IshemaLink API

This document summarizes the key security and compliance decisions implemented for Formative 2.

## Hybrid Authentication
- **Session-based auth** for web dashboard users (Admins & Sector Agents). Auto-logs out when the browser closes to prevent unauthorized access on shared devices.
- **JWT auth** for mobile users (Truck Drivers & Customers) to allow persistent access, even in network "dead zones."
- **Basic Auth** is strictly limited to development/testing environments.
- Rate limiting set to **max 5 login attempts per minute** to prevent brute-force attacks.

## Data Protection
- **Field-level encryption** applied to sensitive fields: `nid_number` and `tax_id`.
- Encryption implemented using `cryptography` (Fernet) for secure at-rest storage.
- Soft-delete mechanism supports GDPR-style "Right to be Forgotten."
- **Audit logs** record every access to sensitive data, including who accessed it and when.

## RBAC & Permissions
- Custom DRF permission classes enforce role-based access:
  - Drivers cannot view pricing or financial information.
  - Sector Agents only access shipments within their assigned districts.
  - RURA/Customs officials have global read-only access.
- Object-level permissions implemented using `get_queryset` filtering and conditional serializer fields.

## OTP & KYC
- OTP verification uses 6-digit codes with a 5-minute expiry stored in Redis.
- Users cannot ship items until `is_verified` is `True`.
- Multi-step verification ensures only verified agents handle high-value cargo.

## Security Headers & Middleware
- HSTS, X-Content-Type-Options added to HTTP headers for secure transport.
- Audit middleware logs all GET requests to sensitive endpoints.
- Throttling applied to authentication endpoints to further protect against attacks.

---

These measures ensure compliance with **Rwanda’s Data Protection Law N° 058/2021** while maintaining usability for low-connectivity users.
