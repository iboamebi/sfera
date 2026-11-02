# Sfera Authentication Foundation

## Status

Backend authentication foundation is implemented.

Implemented:

- user domain entity and repository contract;
- user persistence and mapping;
- password hashing through the application port and Argon2 infrastructure adapter;
- authenticated session domain contract and persistence;
- session token generation;
- authentication and password-change application services;
- login, current-user, password-change, and logout API endpoints;
- mandatory first-login password change state and server-side business-route gate;
- server-managed HttpOnly session cookie;
- CSRF protection for state-changing cookie-authenticated requests;
- reusable API dependency for resolving the current authenticated user;
- authentication + CSRF protection on current business mutation endpoints.

Authorization remains a separate concern and is implemented for concrete business use cases. See `AUTHORIZATION.md` for the role and use-case contract.

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
 ├── role
 ├── is_active
 ├── must_change_password
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
ChangePassword
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
POST /auth/change-password
POST /auth/logout
```

### `POST /auth/login`

Accepts credentials and establishes an authenticated session.

Successful response returns the client-safe authenticated user representation, including `role` and `must_change_password`, without exposing the password hash. A user with `must_change_password = true` receives an authenticated session but cannot access business routes until the password is changed.

Invalid credentials return `401 Unauthorized`.

### `GET /auth/me`

Returns the currently authenticated user.

Unauthenticated requests return `401 Unauthorized`. The response includes the current `role` and `must_change_password` state.

### `POST /auth/change-password`

Requires the authenticated session and CSRF validation. Accepts `current_password` and `new_password`. The Application service verifies the current password, hashes the replacement through the Argon2 password-hasher port, persists the new hash, and clears `must_change_password`. Invalid current passwords return `400 Bad Request`.

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

A reusable API dependency resolves the current authenticated user for protected business routes. The client-safe representation includes the user's role and first-login password-change state.

---

## 8. Protected business routes

Every business router is protected by the API authentication dependency and the first-login password gate. This includes read and write endpoints.

A user with `must_change_password = true` can access only the authentication endpoints needed to complete the flow:

- `POST /auth/login`;
- `GET /auth/me`;
- `POST /auth/change-password`;
- `POST /auth/logout`.

The health endpoint remains public.

State-changing business operations retain their existing CSRF protection.

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

The authentication and first-login gate is applied at the API boundary. Business authorization rules remain in Application use cases and are documented separately in `AUTHORIZATION.md`.

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

Roles and permissions are not defined by this authentication contract. Their current business ownership and enforcement are documented in `AUTHORIZATION.md`.

Business authorization remains enforced at the Application boundary. New permissions are introduced only for concrete business use cases and are documented in `AUTHORIZATION.md`.

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
- API tests for login, current-user, password change, logout, CSRF, first-login gating, and unauthorized access;
- frontend typecheck/build for frontend changes;
- Ruff validation for Python changes.

Security-sensitive behavior must be covered by regression tests before production deployment.

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
First-login password-change gate
    ↓
Authentication tests
    ↓
Current-user API dependency
    ↓
CSRF protection
    ↓
Protected business mutation boundary
```

Business authorization is maintained as a separate contract in `AUTHORIZATION.md`. Frontend authentication and first-login route integration remain a separate implementation stage.

No step may bypass the architectural boundaries defined by the project Constitution.
