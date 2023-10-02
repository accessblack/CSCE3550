# JWT Authentication Server with Flask

This server uses Flask to implement a JWT authentication system with RSA encryption. It generates RSA keys and provides a means to authenticate a user and return a JWT.

## Features:

- Key Generation upon startup.
- Dynamic JWKS endpoint which provides currently valid RSA keys.
- Authentication endpoint for a hardcoded user.

## Dependencies:

- Flask
- PyJWT
- cryptography

## Setup:

1. Ensure you have Python installed on your machine.
2. Install the required dependencies:

```bash
pip install Flask PyJWT cryptography
```

3. Run the server:

```bash
python your_filename.py
```

This will start the server on `http://127.0.0.1:8080/`.

## Endpoints:

### GET `/jwks`

Returns the set of currently valid public RSA keys in JWKS (JSON Web Key Set) format.

Response:

```json
{
    "keys": [
        {
            "kty": "RSA",
            "kid": "1",
            "n": "PUBLIC_KEY_PART_N",
            "e": "PUBLIC_KEY_PART_E"
        }
        // ... additional keys if any
    ]
}
```

### POST `/auth`

Authenticate and receive a JWT.

Request body:

```json
{
    "username": "userABC",
    "password": "password123"
}
```

Query Parameters:

- `expired`: If set, the server will sign the JWT with an already expired key.

Response:

```json
{
    "token": "YOUR_JWT_HERE"
}
```

## Notes:

- The server uses a hardcoded user (`userABC`) and password (`password123`) for authentication. This is just for demonstration purposes and should be replaced with a proper user management system in a real-world application.
- Only one key is generated upon startup, but the code is structured to handle multiple keys.
- Keys are set to expire after 365 days.

## Security:

Ensure to never expose private keys. In a real-world application, private keys should be stored securely and never be hard-coded or exposed through endpoints. Always use HTTPS in production.
