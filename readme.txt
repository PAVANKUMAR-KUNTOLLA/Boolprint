 Boolprint API - Django Application

 Overview

The Boolprint API provides endpoints for user authentication and item management. The API allows users to sign up, log in, manage their profile, and perform CRUD operations on items.

 Endpoints

 1. Signup Endpoint

- **Method**: `POST`
- **Path**: `/base/users/signup/`
- **Description**: This endpoint allows new users to create an account.

**Request Body**:
`{ "username": "test_user", "password": "secure_password", "email": "user@example.com" }`

**Response**:
`{ "id": 1, "username": "test_user", "email": "user@example.com" }`

**Error Codes**:
- `400`: Invalid input (e.g., missing or invalid fields)
- `409`: User already exists

---

 2. Login Endpoint

- **Method**: `POST`
- **Path**: `/base/users/login/`
- **Description**: Authenticates a user and returns an access token.

**Request Body**:
`{ "username": "test_user", "password": "secure_password" }`

**Response**:
`{ "access_token": "eyJhbGciOiJIUzI1NiIs...", "refresh_token": "eyJhbGciOiJIUzI1NiIs..." }`

**Error Codes**:
- `401`: Invalid credentials

---

 3. Profile Endpoint

- **Method**: `GET`
- **Path**: `/base/users/profile/`
- **Description**: Fetches the profile of the authenticated user.

**Headers**:
- `Authorization: Bearer <access_token>`

**Response**:
`{ "id": 1, "username": "test_user", "email": "user@example.com" }`

**Error Codes**:
- `401`: Unauthorized

---

 4. Logout Endpoint

- **Method**: `POST`
- **Path**: `/base/users/logout/`
- **Description**: Logs the user out by invalidating the access and refresh tokens.

**Request Body**:
`{ "refresh_token": "eyJhbGciOiJIUzI1NiIs..." }`

**Response**:
`{ "message": "Successfully logged out" }`

**Error Codes**:
- `400`: Invalid refresh token
- `401`: Unauthorized

---

 Item Management Endpoints

 5. Create Item Endpoint

- **Method**: `POST`
- **Path**: `/items/`
- **Description**: Creates a new item.

**Request Body**:
`{ "name": "Item Name", "description": "Item description" }`

**Response**:
`{ "id": 1, "name": "Item Name", "description": "Item description" }`

**Error Codes**:
- `400`: Item already exists

---

 6. Read Item Endpoint

- **Method**: `GET`
- **Path**: `/items/{item_id}/`
- **Description**: Retrieves details of a specific item by its ID.

**Response**:
`{ "id": 1, "name": "Item Name", "description": "Item description" }`

**Error Codes**:
- `404`: Item not found

---

 7. Update Item Endpoint

- **Method**: `PUT`
- **Path**: `/items/{item_id}/`
- **Description**: Updates the details of a specific item.

**Request Body**:
`{ "name": "Updated Item Name", "description": "Updated item description" }`

**Response**:
`{ "id": 1, "name": "Updated Item Name", "description": "Updated item description" }`

**Error Codes**:
- `404`: Item not found

---

 8. Delete Item Endpoint

- **Method**: `DELETE`
- **Path**: `/items/{item_id}/`
- **Description**: Deletes a specific item by its ID.

**Response**:
`{ "message": "Item deleted successfully" }`

**Error Codes**:
- `404`: Item not found

---

 Authentication & Security

All secured endpoints (like Profile, Create, Update, and Delete Item) require a valid `Authorization` header with a Bearer token, which is obtained via the login endpoint.
