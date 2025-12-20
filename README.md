# Security Assessment: React-Flask-MongoDB Application

**Date:** December 20, 2025
**Author:** Saad Sai El Haq
**Methodology:** Blackbox Penetration Test

## 🛡️ Executive Summary

This repository contains the full Penetration Test Report for a containerized **React-Flask-MongoDB** application. The assessment was conducted using a **Blackbox methodology** against a local deployment (`127.0.0.1`) to identify critical security flaws.

The audit identified **3 key vulnerabilities**, resulting in a **Critical** security posture rating. The findings demonstrate that an unauthenticated attacker could fully compromise the database, delete all data, and access backend credentials.

---

## 🔍 Reconnaissance & Scope

An initial network scan was performed using `nmap` to identify the attack surface on `127.0.0.1`.

**Open Ports Identified:**

- **Port 3000:** Node.js (Frontend)
- **Port 5000:** Gunicorn/Flask (Backend API)

---

## 🚨 Vulnerability Findings

### 1. [CRITICAL] Broken Access Control (Insecure Deletion)

**Description:**
The API endpoint `DELETE /api/task/<id>` lacks any authentication checks. An anonymous attacker can delete any task simply by knowing its ID.

**Proof of Concept:**
The following `curl` command successfully deleted a task without a token:

```bash
curl -X DELETE -v http://127.0.0.1:5000/api/task/694683af4d6867e0cabfd229
```

**Impact:** Complete loss of data integrity and availability. A script could wipe the entire database in minutes, causing catastrophic data loss.

---

### 2. [HIGH] Hardcoded Credentials

**Description:**
Database credentials were found hardcoded in plaintext within the `docker-compose.yml` file and exposed via environment variables.

**Evidence:**

```yaml
MONGO_INITDB_ROOT_USERNAME: assia
MONGO_INITDB_ROOT_PASSWORD: test
```

**Impact:** Violates confidentiality. If leaked into version control (e.g., GitHub), attackers gain administrative access to the database to steal or modify data.

---

### 3. [MEDIUM] Missing Rate Limiting

**Description:**
The API does not restrict the number of requests a user can make in a given timeframe.

**Proof of Concept:**
Server resources were exhausted by flooding the endpoint with thousands of POST requests per second using a simple loop:

```bash
while true; do
    curl -X POST -H "Content-Type: application/json" \
    -d '{"title":"DoS Attack"}' \
    http://127.0.0.1:5000/api/task > /dev/null &
done
```

**Impact:** High vulnerability to Denial of Service (DoS) and Brute Force attacks, potentially making the website unreachable for legitimate users.

---

## 🛠️ Recommendations

To remediate these vulnerabilities, the following actions are recommended:

- **Implement Authentication:** Use JWT (JSON Web Tokens) to verify user identity before allowing DELETE or PUT operations.
- **Secrets Management:** Move credentials to a `.env` file and exclude it from version control.
- **Enable Rate Limiting:** Implement Flask-Limiter to restrict request frequency (e.g., 100 requests per minute per IP).

---

_This report is for educational and remediation purposes only._
