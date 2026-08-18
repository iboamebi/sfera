# Sfera Authentication Foundation

## Status

Backend authentication foundation is implemented.

Implemented:

- user domain entity and repository contract;
- user persistence and mapping;
- password hashing through the application port and Argon2 infrastructure adapter;
- authenticated session domain contract and persistence;
- session token generation;
- authentication application services;
- login, current-user, and logout API endpoints;
- server-managed HttpOnly session cookie;
- CSRF protection for state-changing cookie-authenticated requests;
- reusable API dependency for resolving the current authenticated user;
- authentication + CSRF protection on current business mutation endpoints.

Authorization (roles/permissions) is intentionally not implemented yet. It remains a separate stage.

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

The authenticated identity is a Sfera user.

Minimum persistent user data:

```text
User
 ├── id
 ├── username
 ├── password_hash
 ├── archived
 └── created_at
```

Archived users must not authenticate.

User passwords are never stored in plaintext.

---

## 4. Authentication mechanism

The application uses a server-managed authenticated session represented to the browser by an HttpOnly cookie.

The browser is not required to store an access token in `localStorage` or `sessionStorage`.

The session cookie is configured by the API layer according to the deployment security contract.

Authentication includes session invalidation on logout and session creation through the Application service.

CSRF protection is required for state-changing cookie-authenticated requests and is implemented through the API security boundary.

---

## 5. Application use cases

The authentication use cases are:

```text
AuthenticateUser
CreateSession
GetCurrentUser
RevokeSession
LogoutUser
```

Application services/use cases operate through repository abstractions and do not manipulate SQLAlchemy sessions directly.

A failed authentication attempt returns a generic authentication failure and does not reveal whether a username exists.

---

## 6. API contract

The public authentication API is:

```text
POST /auth/login
GET  /auth/me
POST /auth/logout
```

### `POST /auth/login`

Accepts credentials and establishes an authenticated session.

Successful response returns the current authenticated user representation without exposing the password hash.

Invalid credentials return `401 Unauthorized`.

### `GET /auth/me`

Returns the currently authenticated user.

Unauthenticated requests return `401 Unauthorized`.

### `POST /auth/logout`

Invalidates the current authenticated session.

The endpoint is idempotent from the client perspective and is protected by CSRF validation.

---

## 7. Current-user contract

The API representation of the authenticated user contains only client-safe identity data.

It must never expose:

- password hash;
- password reset secrets;
- session identifiers;
- internal authentication metadata.

A reusable API dependency resolves the current authenticated user for protected business routes.

---

## 8. Protected business mutations

The current API security boundary protects state-changing business operations with both authentication and CSRF validation.

Protected mutation features currently include:

```text
Customer
Organization
Order
Device
Repair
Diagnostic
Warehouse
Material
PriceList
PriceListItem
InstrumentType
Verification actions
```

Read-only endpoints remain unchanged unless a separate business authorization requirement is introduced.

The protection is applied at the API boundary; business rules remain in Application/Domain layers.

---

## 9. Authorization boundary

Authentication answers:

```text
Who is the user?
```

Authorization answers:

```text
What may the user do?
```

Roles and permissions are intentionally not defined by the authentication foundation yet.

The next security stage is authorization at the Application/API boundary, without embedding permission checks throughout UI components or domain entities.

---

## 10. Frontend integration

Frontend authentication remains a separate integration stage:

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

The backend authentication contract exists; frontend auth API/model and login UI still require implementation and validation as a separate feature stage.

---

## 11. Validation requirements

Authentication changes require at minimum:

- Domain/Application tests for authentication behavior;
- Infrastructure tests for password/session persistence where applicable;
- API tests for login, current-user, logout, CSRF, and unauthorized access;
- frontend typecheck/build for frontend changes;
- Ruff validation for Python changes.

Security-sensitive behavior must be covered by regression tests before production deployment.

Current backend validation checkpoint:

```text
pytest: 105 passed
ruff check: clean
ruff format --check: clean
```

---

## 12. Implementation order

The completed implementation path is:

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
Current-user API dependency
    ↓
CSRF protection
    ↓
Protected business mutation boundary
```

The next stage is intentionally separate:

```text
Authorization
    ↓
roles/permissions contract
    ↓
Application authorization policy
    ↓
API enforcement
    ↓
regression tests
```

No step may bypass the architectural boundaries defined by the project Constitution.
