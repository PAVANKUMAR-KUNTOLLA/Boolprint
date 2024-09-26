Boolprint API - Postman Collection
This collection contains requests for interacting with the Boolprint API for managing user authentication and item management. The collection includes endpoints for user signup, login, profile management, and item CRUD operations.

Collection Structure
1. Signup (POST)
Endpoint: http://127.0.0.1:8000/base/users/signup/
Method: POST
Description: Allows new users to create an account by submitting necessary signup information like email, password, and other details.
Request Body: You need to provide user credentials and any other required signup fields.
Response: Returns a response confirming account creation, usually including a user ID or token for authentication.
2. Login (GET)
Method: GET
Description: This is a placeholder and does not yet include any URL or parameters. It would typically allow users to log in by submitting valid credentials (e.g., username/email and password) and receive an access token.
3. Profile (POST)
Endpoint: http://127.0.0.1:8000/base/users/profile/
Method: POST
Headers: Requires an Authorization header with a valid JWT token (Bearer token).
Description: This request allows the authenticated user to access or update their profile information. You need to be logged in to access this endpoint.
Request Body: Provide the necessary profile fields to be updated.
Response: Returns the updated profile details or an error if the token is invalid or expired.
4. Logout (POST)
Endpoint: http://127.0.0.1:8000/base/users/logout/
Method: POST
Headers: Requires an Authorization header with a valid JWT token.
Description: Logs the user out by invalidating their access token. A refresh token should also be sent in the request body to be invalidated.
Request Body:
json
Copy code
{
    "refresh_token": "<valid_refresh_token>"
}
Response: Confirms that the tokens have been invalidated and the user has been logged out successfully.
5. ItemCreation (GET)
Method: GET
Description: This request currently lacks a URL or detailed information. It would typically allow the creation of an item in the system by sending the required data, like item name, description, and any other necessary fields.
Response: Returns confirmation of item creation, along with item details.
6. RetrieveItem (GET)
Method: GET
Description: This request lacks a URL and is intended to retrieve a specific item based on its ID or some identifying parameter.
Response: Returns the details of the requested item, including all its properties and related information.
7. ItemUpdate (GET)
Method: GET
Description: This request is used to update an existing item. Typically, it would require the item ID in the URL and the fields that need updating.
Response: Confirms the update and returns the updated item details.
8. DeleteItem (GET)
Method: GET
Description: This is a placeholder for deleting an item. You would typically need the item ID in the URL to identify which item to delete.
Response: Confirms successful deletion of the item.
