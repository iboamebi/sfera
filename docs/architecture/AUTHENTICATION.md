# Sfera Authentication Foundation

## Status

Foundation contract.

Authentication is not yet implemented in the application runtime.

This document defines the minimum contract that future authentication changes must follow.

---

## 1. Purpose

Authentication establishes the identity of the current Sfera user.

Authorization is a separate concern and must not be introduced implicitly into the authentication implementation.

Business use cases remain in the Application layer and must not depend on HTTP-specific authentication details.

---

## 2. Architecture

Authentication follows the project architecture:

```text
API
  ↓
Application
  ↓
Domain
  ↓
Repository Interface
  ↑
Infrastructure Repository
  ↓
Database
```

Security mechanisms such as password hashing, token/session handling, cookie configuration, and HTTP authentication adapters belong to Infrastructure/API boundaries as appropriate.

Domain must not depend on FastAPI, SQLAlchemy, HTTP cookies, JWT libraries, or password-hashing libraries.

---

## 3. Identity

The initial authenticated identity is a Sfera user.

Minimum persistent user data:

```text
User
 ├── id
 ├── username
 ├── password_hash
 ├── archived
 └── created_at
```

The exact additional profile fields are outside the authentication foundation and should be introduced only when required by a user-facing scenario.

Archived users must not authenticate.

User passwords are never stored in plaintext.

---

## 4. Authentication mechanism

The initial application contract uses a server-managed authenticated session represented to the browser by an HttpOnly cookie.

The browser must not be required to store an access token in `localStorage` or `sessionStorage`.

The session cookie must be configured by the API layer/Infrastructure with secure production attributes appropriate to the deployment.

Authentication implementation must include protection against session fixation and must invalidate the session on logout.

CSRF protection is required for state-changing cookie-authenticated requests.

---

## 5. Application use cases

The initial authentication use cases are:

```text
AuthenticateUser
GetCurrentUser
LogoutUser
```

Application services/use cases must operate through repository abstractions and must not manipulate SQLAlchemy sessions directly.

A failed authentication attempt returns a generic authentication failure and must not reveal whether a username exists.

---

## 6. API contract

The initial public API contract is:

```text
POST /auth/login
GET  /auth/me
POST /auth/logout
```

Expected semantics:

### `POST /auth/login`

Accepts credentials and establishes an authenticated session.

Successful response returns the current authenticated user representation without exposing the password hash.

Invalid credentials return `401 Unauthorized`.

### `GET /auth/me`

Returns the currently authenticated user.

Unauthenticated requests return `401 Unauthorized`.

### `POST /auth/logout`

Invalidates the current authenticated session.

The endpoint is idempotent from the client perspective.

---

## 7. Current user contract

The API representation of the authenticated user must contain only client-safe identity data.

It must never expose:

- password hash;
- password reset secrets;
- session identifiers;
- internal authentication metadata.

The frontend consumes this representation through an API feature/model and does not reproduce authentication business rules locally.

---

## 8. Authorization boundary

Authentication answers:

```text
Who is the user?
```

Authorization answers:

```text
What may the user do?
```

The first authentication iteration does not define roles or permissions unless an existing business scenario requires them.

Future authorization must be enforced at the Application/API boundary without embedding permission checks throughout UI components.

---

## 9. Frontend integration

Frontend authentication will follow:

```text
API
 ↓
Auth feature
 ↓
Current-user query
 ↓
Auth state
 ↓
Protected route boundary
 ↓
User interface
```

The frontend HTTP client must send authenticated requests according to the server session contract.

The frontend must treat `401 Unauthorized` as an authentication state transition, not as a generic business error.

Login UI is not part of this foundation document and should be introduced only after the backend contract exists.

---

## 10. Validation requirements

Authentication changes require at minimum:

- Domain/Application tests for authentication behavior;
- Infrastructure tests for password/session persistence where applicable;
- API tests for login, current-user, logout, and unauthorized access;
- frontend typecheck/build for frontend changes;
- Ruff validation for Python changes.

Security-sensitive behavior must be covered by regression tests before production deployment.

---

## 11. Implementation order

Authentication implementation proceeds incrementally:

```text
User domain contract
    ↓
User repository interface
    ↓
Infrastructure persistence
    ↓
Password hashing/session infrastructure
    ↓
Application authentication use cases
    ↓
API authentication endpoints
    ↓
Authentication tests
    ↓
Frontend auth API/model
    ↓
Protected route boundary
    ↓
Login UI
```

No step may bypass the architectural boundaries defined by the project Constitution.
