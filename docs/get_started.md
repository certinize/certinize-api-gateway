## Authorization

Authorization is a one-step process. You should be able to access most endpoints by attaching your wallet address to the `/users` endpoint as a path parameter and making an HTTP GET request.

Example request:
```
/users/9ZNTfG4NyQgxy2SWjSiQoUyBPEvXT2xo7fKc5hPYYJ7b
```

The server should then return an associated API key (UUID).

Example response:

```json
{
  "wallet_address": "9ZNTfG4NyQgxy2SWjSiQoUyBPEvXT2xo7fKc5hPYYJ7b",
  "api_key": "e8e5725b-7f33-5bad-9438-e63bdbd2efea",
  "user_id": "5ca167d6-1654-11ed-908f-00155d3ecff4"
}
```
