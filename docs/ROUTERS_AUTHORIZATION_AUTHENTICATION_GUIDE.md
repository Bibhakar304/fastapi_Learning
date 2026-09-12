# FastAPI Routers, Authentication, and Authorization Guide

This guide explains how to evolve the current FastAPI project from one `main.py` file into a maintainable API with routers, authentication, and authorization.

The goal is to understand the responsibility of each layer before implementing it.

## 1. Current Project

The project currently contains:

- `main.py`: creates the FastAPI application and defines user endpoints.
- `database.py`: creates the SQLAlchemy engine, session factory, and `get_db()` dependency.
- `model.py`: contains the SQLAlchemy `User` model.
- `schemas.py`: contains Pydantic request and response models.
- `repository.py`: contains database operations such as creating and finding users.

The current request flow is:

```text
HTTP request
    -> main.py route
    -> get_db() dependency
    -> repository function
    -> SQLAlchemy model
    -> MySQL database
```

The next goal is:

```text
HTTP request
    -> router
    -> authentication dependency, when required
    -> authorization dependency, when required
    -> repository/service logic
    -> database
```

## 2. Router: What and Why?

A router is a separate group of related endpoints. It keeps `main.py` small and organizes the application by feature.

Instead of putting every endpoint in `main.py`, use feature routers:

```text
routers/
    users.py
    auth.py
```

A router owns HTTP concerns:

- URL paths
- HTTP methods
- request and response schemas
- dependencies
- status codes
- calling service or repository functions

`main.py` should mainly create the app and include routers.

### Example Router Shape

```python
# routers/users.py
from fastapi import APIRouter

router = APIRouter(prefix="/users", tags=["Users"])

@router.get("/{user_id}")
def get_user(user_id: int):
    ...
```

Register it in the application:

```python
# main.py
from routers import users

app.include_router(users.router)
```

With the prefix, the endpoint becomes:

```text
GET /users/{user_id}
```

### Recommended Router Groups

Start with:

```text
routers/
    auth.py       # register, login, current-user endpoints
    users.py      # user profile and user administration endpoints
```

Later, add routers such as `items.py`, `orders.py`, or `admin.py` when the project grows.

## 3. Authentication Versus Authorization

These concepts are related but different.

### Authentication

Authentication answers:

> Who is making this request?

Examples:

- A user sends a username and password to `/auth/login`.
- The server verifies the password.
- The server creates an access token.
- The client sends the token on future requests.

Typical status code for failed authentication:

```text
401 Unauthorized
```

### Authorization

Authorization answers:

> Is this authenticated user allowed to perform this action?

Examples:

- Any logged-in user can view their own profile.
- Only an administrator can delete another user.
- A user cannot update another user's private data.

Typical status code for failed authorization:

```text
403 Forbidden
```

The sequence is:

```text
Authentication: identify the user
Authorization: check the user's permissions
```

## 4. Recommended Application Structure

A practical next structure is:

```text
FastAPI/
    main.py
    database.py
    model.py
    schemas.py
    repository.py
    security.py
    dependencies.py
    routers/
        __init__.py
        auth.py
        users.py
```

For a larger application, separate the user code further:

```text
app/
    main.py
    database.py
    models/
        user.py
    schemas/
        user.py
        auth.py
    repositories/
        user.py
    routers/
        auth.py
        users.py
    core/
        security.py
        config.py
```

Do not create all of these folders at once. First move the existing endpoints into routers, verify them, and then add authentication.

## 5. Router Migration Plan

### Step 1: Create the Router Package

Create:

```text
routers/
    __init__.py
    users.py
```

Move the current `POST /users` and `GET /users/{user_id}` route functions from `main.py` to `routers/users.py`.

The router should import:

```python
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from database import get_db
from repository import create_user, get_user_by_id
from schemas import UserCreate, UserResponse
```

Use a router prefix:

```python
router = APIRouter(prefix="/users", tags=["Users"])
```

### Step 2: Add the Router to `main.py`

Keep only application setup and router registration in `main.py`:

```python
from fastapi import FastAPI
from routers import users

app = FastAPI(...)
app.include_router(users.router)
```

### Step 3: Add Response Models

A route should declare what it returns:

```python
@router.post("", response_model=UserResponse, status_code=201)
def create_user(...):
    ...
```

Do not return the password in `UserResponse`.

This makes the API contract explicit and prevents accidental sensitive data from being returned.

## 6. Password Storage Rules

Never store a plain-text password in the database.

Current code passes the password directly into the `User` model. Before adding login, replace this with password hashing.

The correct flow is:

```text
Registration:
    plain password
        -> password hash
        -> store only the hash

Login:
    plain password from request
        -> compare with stored hash
        -> issue token if valid
```

Use a password hashing library such as `pwdlib` with Argon2, or another actively maintained password hashing library.

The database should contain something like a password hash, never the original password.

A future model field should be named clearly:

```python
hashed_password: Mapped[str] = mapped_column(String(255), nullable=False)
```

A migration or table update will be required when renaming the current `password` column.

## 7. Authentication Flow with JWT

A common learning-friendly flow is JWT bearer authentication.

### Registration

```text
POST /auth/register
    -> validate input
    -> check whether email/username already exists
    -> hash password
    -> save user
    -> return safe user data
```

### Login

```text
POST /auth/login
    -> receive username/email and password
    -> find user
    -> verify password hash
    -> create access token
    -> return access token
```

Example response:

```json
{
  "access_token": "<token>",
  "token_type": "bearer"
}
```

### Authenticated Request

The client sends:

```http
Authorization: Bearer <access-token>
```

The server then:

```text
extract bearer token
    -> decode and validate JWT
    -> read user identity from token
    -> load user from database
    -> provide current user to the route
```

## 8. Security Components

Create a `security.py` module for security-only functions:

```text
security.py
    hash_password(password)
    verify_password(password, password_hash)
    create_access_token(data)
    decode_access_token(token)
```

Keep token creation and password hashing out of route functions. This makes them easier to test and reuse.

Use environment variables for secrets:

```text
SECRET_KEY=<long-random-secret>
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
```

Never commit a real secret, database password, or token to source control.

## 9. Current User Dependency

Create a dependency that converts a valid bearer token into a database user.

Conceptually:

```python
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/login")


def get_current_user(
    token: str = Depends(oauth2_scheme),
    db: Session = Depends(get_db),
):
    # decode token
    # extract user id or username
    # load user from database
    # reject invalid or missing users
    return user
```

Routes use it like this:

```python
@router.get("/me", response_model=UserResponse)
def get_current_user_profile(current_user = Depends(get_current_user)):
    return current_user
```

This dependency is authentication. It establishes who the caller is.

## 10. Authorization with Roles

Add a role to the user model, for example:

```python
role: Mapped[str] = mapped_column(String(20), default="user", nullable=False)
```

Possible roles:

```text
user
admin
```

Then create a role-checking dependency:

```python
def require_admin(current_user = Depends(get_current_user)):
    if current_user.role != "admin":
        raise HTTPException(
            status_code=403,
            detail="Administrator permission required",
        )
    return current_user
```

Use it on protected routes:

```python
@router.delete("/{user_id}")
def delete_user(
    user_id: int,
    db: Session = Depends(get_db),
    current_user = Depends(require_admin),
):
    ...
```

The dependency chain is:

```text
require_admin
    -> get_current_user
        -> OAuth2 bearer token
            -> database user
```

## 11. Ownership Authorization

Roles are not the only authorization rule. Often a user may access only their own record.

Example rule:

```python
if current_user.user_id != user_id and current_user.role != "admin":
    raise HTTPException(status_code=403, detail="Access denied")
```

This protects against a user changing the URL to another user's ID.

Authorization must be checked on the server. Never trust a user ID sent by the client without comparing it to the authenticated identity.

## 12. Correct HTTP Errors

Use clear status codes:

| Situation | Status |
|---|---:|
| Invalid request body | 422 |
| Missing or invalid token | 401 |
| Valid user without permission | 403 |
| User does not exist | 404 |
| Duplicate username/email | 409 |
| Database unavailable | 503 |
| Unexpected server error | 500 |

For authentication failures, include the bearer authentication header when appropriate so clients know authentication is required.

## 13. Database Error Handling

The current project already handles `SQLAlchemyError` globally in `main.py` and rolls back failed writes in `repository.py`.

Keep these rules:

- Always call `rollback()` after a failed transaction.
- Do not expose SQL statements, passwords, or full tracebacks to API clients.
- Log the full error on the server.
- Return a safe, useful error message to the client.
- Handle duplicate records separately when possible and return `409 Conflict`.

## 14. Dependency and Configuration Checklist

Before implementing authentication, install the selected libraries in the virtual environment.

The exact package choice can vary, but the project will need:

```text
FastAPI
SQLAlchemy
PyMySQL
Pydantic email support
password hashing library
JWT library
```

Move database and JWT configuration out of Python source code and into environment variables. Use `pydantic-settings` for configuration.

Example configuration values:

```text
DATABASE_URL=mysql+pymysql://...
SECRET_KEY=...
ACCESS_TOKEN_EXPIRE_MINUTES=30
```

## 15. Recommended Implementation Order

Implement and test one stage at a time:

1. Confirm MySQL connection and the `users` table.
2. Move existing user routes into `routers/users.py`.
3. Register the router in `main.py`.
4. Add response models and make sure passwords are excluded.
5. Add password hashing for registration.
6. Add `/auth/register`.
7. Add `/auth/login` and token creation.
8. Add `get_current_user` authentication dependency.
9. Protect `GET /users/me`.
10. Add user roles and admin authorization.
11. Add ownership checks for user-specific resources.
12. Add tests for success, invalid credentials, missing token, insufficient permissions, duplicate users, and database failures.

Do not add JWT before password hashing and user lookup work correctly. Otherwise several failures will appear at the same time and become difficult to understand.

## 16. Debugging Each Stage

Start the server with detailed logging:

```bash
.venv/bin/uvicorn main:app --reload --log-level debug
```

Check application import first:

```bash
.venv/bin/python -c "import main; print('Application import: OK')"
```

Then test in this order:

```text
GET /
GET /docs
POST /users
GET /users/{user_id}
POST /auth/register
POST /auth/login
GET /users/me with Authorization header
Admin-only endpoint with user token
Admin-only endpoint with admin token
```

When reading a traceback:

1. Start at the final exception message.
2. Find the first file path belonging to this project.
3. Inspect the line that called the failing library operation.
4. Check the values passed to that line.
5. Reproduce the smallest failing operation.

Useful temporary breakpoints are:

- before `db.commit()`
- after loading a user
- after verifying a password
- after decoding a token
- inside authorization checks

## 17. Minimum Security Rules

- Never store plain-text passwords.
- Never return password hashes in API responses.
- Never hard-code production secrets.
- Use HTTPS in production.
- Keep access tokens short-lived.
- Validate token expiration.
- Return `401` for invalid authentication.
- Return `403` for insufficient permissions.
- Do not trust role values sent by clients.
- Log security failures without logging passwords or tokens.
- Use database constraints for unique usernames and emails.

## 18. Target Endpoints

A reasonable first target API is:

```text
POST /auth/register       public
POST /auth/login          public
GET  /users/me             authenticated user
GET  /users/{user_id}      authenticated, ownership or admin check
DELETE /users/{user_id}   admin only
```

The important design principle is to keep responsibilities separate:

```text
Router:
    HTTP request and response

Dependency:
    database session, current user, permission checks

Security module:
    password hashing and JWT operations

Repository:
    database queries and persistence

Model:
    database table structure

Schema:
    input and output validation
```

This separation makes each piece easier to understand, debug, and test.
