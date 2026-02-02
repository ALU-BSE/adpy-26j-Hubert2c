# Threat Model for IshemaLink API

This document identifies potential security risks and mitigation strategies for the IshemaLink logistics platform.

---

## 1. Insider Threat – Rogue Agent
**Risk:** Sector Agents may attempt to manipulate shipments or access unauthorized districts.  
**Mitigation:** 
- Role-Based Access Control (RBAC) restricts data access by assigned district.
- Object-level permissions prevent access to unrelated shipments.
- Audit logs record every access to sensitive data.
- Multi-step KYC verification ensures only verified agents can release cargo.

---

## 2. Credential Theft – Brute Force / Phishing
**Risk:** Attackers may try to gain access using stolen credentials or by guessing passwords.  
**Mitigation:** 
- Rate limiting on login endpoints (maximum 5 attempts per minute).
- Hybrid authentication: Sessions for web, JWT for mobile apps.
- OTP verification adds an extra layer for critical actions (e.g., password reset, shipment release).

---

## 3. Data Leakage – Sensitive Cargo & NIDs
**Risk:** Exposure of customer NIDs, tax IDs, or high-value shipment information.  
**Mitigation:** 
- Field-level encryption for NID and tax ID fields using `cryptography` (Fernet).
- Audit middleware logs all GET requests to sensitive endpoints.
- Right-to-forget functionality anonymizes user data upon request.
- Encrypted storage ensures sensitive data is never stored in plaintext.

---

## 4. Notes
- All sensitive endpoints should be accessed over HTTPS in production.
- Regular dependency updates and code reviews reduce vulnerability surface.
- Logging and monitoring provide early detection of abnormal or suspicious activity.
- Admins and auditors have controlled access to compliance reports and audit logs only.

---

This threat model ensures IshemaLink complies with **Rwanda’s Data Protection Law N° 058/2021** while protecting both sensitive data and operational integrity.
