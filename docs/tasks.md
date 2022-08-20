## Certificates

### Generate eCertificate

    - Method: POST
    - Path: /certificates
    - Summary: Generate an e-Certificate.

**Request**

Supported Media Types:

- `application/json`

**Response**

Supported Media Types:

- `application/json`

**Response Status Codes**

- 201 Response: The e-Certificate(s) was created.
- 400 Response: Bad request syntax or unsuported method.

**Examples**

Request Header:

```
X-API-Key: 0ef3c43d-a3ac-52a1-938b-57cff7e60282
```

Request Body:

```json
{
  "template_config_id": "36b91a30-16fb-11ed-8a9e-00155d3ecff4",
  "issuance_date": "2022-01-31",
  "recipients": [
    {
      "recipient_name": "Juan Cruz",
      "email_address": "juan_cruz@email.com",
      "wallet_address": "9ZNTfG4NyQgxy2SWjSiQoUyBPEvXT2xo7fKc5hPYYJ7b"
    }
  ]
}
```

HTTP Status Code:

```
201
```

JSON Response:

```json
{
  "certificate_collection_id": "6a5cfab5-6451-4515-abb3-c6bd4033e21e",
  "template_id": "e82fbcd5-3f45-483e-887b-5ffec0194c42",
  "template_url": "https://bucket.s3.objectstorageprovider.com/certificate_template.jpg",
  "template_config_id": "36b91a30-16fb-11ed-8a9e-00155d3ecff4",
  "recipient_name_position": {
    "x": 960,
    "y": 540
  },
  "issuance_date_position": {
    "x": 130,
    "y": 950
  },
  "issuance_date": "2022-01-31",
  "recipients": [
    {
      "recipient_name": "Juan Cruz",
      "email_address": "juan_cruz@email.com",
      "wallet_address": "9ZNTfG4NyQgxy2SWjSiQoUyBPEvXT2xo7fKc5hPYYJ7b",
      "generated_certificate": "https://bucket.s3.objectstorageprovider.com/generated_certificate.jpg"
    }
  ]
}
```

## Configurations

### Create Template Configuration

    - Method: POST
    - Path: /configurations
    - Summary: Save an e-Certificate template configuration.

**Request**

Supported Media Types:

- `application/json`

**Response**

Supported Media Types:

- `application/json`

**Response Status Codes**

- 201 Response: The e-Certificate template configuration was created.
- 400 Response: Bad request syntax or unsuported method.

**Examples**

Request Header:

```
X-API-Key: 0ef3c43d-a3ac-52a1-938b-57cff7e60282
```

Request Body:

```json
{
  "recipient_name": {
    "position": {
      "x": 960,
      "y": 540
    },
    "font_size": 24
  },
  "issuance_date": {
    "position": {
      "x": 130,
      "y": 950
    },
    "font_size": 12
  },
  "template_id": "e82fbcd5-3f45-483e-887b-5ffec0194c42",
  "template_config_name": "example",
  "font_id": "8082c1c8-1e33-11ed-b68e-8bb3135194ad"
}
```

HTTP Status Code:

```
201
```

JSON Response:

```json
{
  "template_config_id": "36b91a30-16fb-11ed-8a9e-00155d3ecff4",
  "template_config_name": "example",
  "config_meta": {
    "recipient_name": {
      "position": {
        "x": 960,
        "y": 540
      },
      "font_size": 24
    },
    "issuance_date": {
      "position": {
        "x": 130,
        "y": 950
      },
      "font_size": 12
    },
    "template_id": "e82fbcd5-3f45-483e-887b-5ffec0194c42",
    "font_id": "8082c1c8-1e33-11ed-b68e-8bb3135194ad"
  }
}
```

### Get Template Configuration

    - Method: GET
    - Path: /configurations/{template_config_id:uuid}
    - Summary: Get a specific template configuration.

**Request**

Path Parameters:

```
template_config_id:uuid
```

**Response**

Supported Media Types:

- `application/json`

**Response Status Codes**

- 200 Response: The request was fulfilled.
- 400 Response: Bad request syntax or unsuported method.

**Examples**

Request Header:

```
X-API-Key: 0ef3c43d-a3ac-52a1-938b-57cff7e60282
```

Request Parameter:

```
/configurations/6e9fd408-207d-11ed-9d54-00155d886c22
```

HTTP Status Code:

```
200
```

JSON Response:

```json
{
  "config_meta": {
    "recipient_name": {
      "position": {
        "x": 960,
        "y": 540
      },
      "font_size": 24
    },
    "issuance_date": {
      "position": {
        "x": 130,
        "y": 950
      },
      "font_size": 12
    }
  },
  "font_id": "e632f180-2056-11ed-b912-bb65d3909f61",
  "template_config_id": "6e9fd408-207d-11ed-9d54-00155d886c22",
  "template_config_name": "my template",
  "template_id": "89b22a51-2057-11ed-9d28-00155d886c22"
}
```

### List Template Configurations

    - Method: GET
    - Path: /configurations
    - Summary: Get a list of template configurations.

**Request**

There are no request parameters for this operation.

**Response**

Supported Media Types:

- `application/json`

**Response Status Codes**

- 200 Response: The request was fulfilled.
- 400 Response: Bad request syntax or unsuported method.

**Examples**

Request Header:

```
X-API-Key: 0ef3c43d-a3ac-52a1-938b-57cff7e60282
```

Request Path:

```
/configurations
```

HTTP Status Code:

```
200
```

JSON Response:

```json
{
  "configurations": [
    {
      "template_config_id": "6e9fd408-207d-11ed-9d54-00155d886c22",
      "template_config_name": "my template",
      "font": {
        "font_id": "e632f180-2056-11ed-b912-bb65d3909f61",
        "font_url": "https://..."
      },
      "template": {
        "template_height": 720,
        "template_id": "89b22a51-2057-11ed-9d28-00155d886c22",
        "template_name": "template_name",
        "template_path": "/certinize-bucket/template_name",
        "template_size": 97583,
        "template_thumbnail_url": "https://...",
        "template_url": "https://...",
        "template_width": 1040
      },
      "template_config": {
        "config_meta": {
          "recipient_name": {
            "position": {
              "x": 960,
              "y": 540
            },
            "font_size": 24
          },
          "issuance_date": {
            "position": {
              "x": 130,
              "y": 950
            },
            "font_size": 12
          }
        },
        "font_id": "e632f180-2056-11ed-b912-bb65d3909f61",
        "template_id": "89b22a51-2057-11ed-9d28-00155d886c22"
      }
    }
  ]
}
```

## Fonts

### Get All Fonts

    - Method: GET
    - Path: /fonts
    - Summary: Retrieve all usable e-Certificate fonts.

**Request**

There are no request parameters for this operation.

**Response**

Supported Media Types:

- `application/json`

**Response Status Codes**

200 Response: The request was fulfilled.
400 Response: Bad request syntax or unsuported method.

**Examples**

Request Header:

```
X-API-Key: 0ef3c43d-a3ac-52a1-938b-57cff7e60282
```

Request Path:

```
/fonts
```

HTTP Status Code:

```
200
```

JSON Response:

```json
{
  "fonts": [
    {
      "font_id": "8082c1c8-1e33-11ed-b68e-8bb3135194ad",
      "font_url": "https://raw.githubusercontent.com/certinize/fonts/main/ttf/example-ttf.ttf"
    },
    ...
  ]
}
```

## Issuances

### Transfer Certificate

    - Method: POST
    - Path: /issuances
    - Summary: Transfer an e-Certificate to a recipient(s). 
    - Description: Transfer generated e-Certificate(s) inside an e-Certificate collection. The recipient(s) is indicated in the collection metadata.

**Request**

Path Parameters:

```
certificate_collection_id:uuid
```

**Response**

Supported Media Types:

- `application/json`

**Response Status Codes**

- 201 Response: The transfer request was fulfilled.
- 400 Response: Bad request syntax or unsuported method.

**Examples**

Request Header:

```
X-API-Key: 0ef3c43d-a3ac-52a1-938b-57cff7e60282
```

Request Parameter:

```
/issuances/34f8ba1a-1707-11ed-a111-f73a0f2a24a8
```

HTTP Status Code:

```
201
```

JSON Response:

```json
{
  "transfer_id": "9b5ec38f-4d0f-4a8b-9a36-60feba6ea7b1",
  "template_id": "e82fbcd5-3f45-483e-887b-5ffec0194c42",
  "template_config_id": "36b91a30-16fb-11ed-8a9e-00155d3ecff4",
  "issuance_date": "2022-01-31",
  "recipients": [
    {
      "recipient_name": "Juan Cruz",
      "email_address": "juan_cruz@email.com",
      "wallet_address": "9ZNTfG4NyQgxy2SWjSiQoUyBPEvXT2xo7fKc5hPYYJ7b",
      "certificate_id": "8561b082-bcdd-4ff0-9506-ee1dcebda715"
    }
  ]
}
```

## Templates

### Add eCertificate Template

    - Method: POST
    - Path: /templates
    - Summary: Upload an e-Certificate template(s).

**Request**

There are no request parameters for this operation.

Supported Media Types:

- `multipart/form-data`

**Response**

Supported Media Types:

- `application/json`

**Response Status Codes**

- 201 Response: The e-Certificate template(s) was uploaded.
- 400 Response: Bad request syntax or unsuported method.

**Examples**

Request Header:

```
X-API-Key: 0ef3c43d-a3ac-52a1-938b-57cff7e60282
```

Form Data:

```
Key: image
Value: C:/path/to/file/template1.png
```

HTTP Status Code:

```
201
```

JSON Response:

```json
{
  "template_height": 1200,
  "template_id": "1a62a09e-1a46-11ed-b3e0-00155d3fe822",
  "template_name": "18a46f27-1a46-11ed-af20-00155d3fe822_wmPgJS8wq",
  "template_path": "/certinize-bucket/18a46f27-1a46-11ed-af20-00155d3fe822_wmPgJS8wq",
  "template_size": 379611,
  "template_thumbnail_url": "https://...",
  "template_url": "https://...",
  "template_width": 773
}
```

For multiple file uploads, the response will contain a list of template metadata: 

```json
{
  "templates": [
    {
      "template_height": 1200,
      ...
    },
    ...
  ]
}
```

### List Templates

    - Method: GET
    - Path: /templates
    - Summary: Get a list of e-Certificate templates.
    - Description: This will list all recorded e-Certificate templates.

**Request**

There are no request parameters for this operation.

Supported Media Types:

- `application/json`

**Response Status Codes**

- 200 Response: The request was fulfilled.
- 400 Response: Bad request syntax or unsuported method.

**Examples**

Request Header:

```
X-API-Key: 0ef3c43d-a3ac-52a1-938b-57cff7e60282
```

Request Parameter:

```
/templates
```

HTTP Status Code:

```
200
```

JSON Response:

```json
{
  "templates": [
    {
      "template_id": "e82fbcd5-3f45-483e-887b-5ffec0194c42",
      "template_url": "http://bucket.s3.provider.com/template.png"
    }
  ]
}
```

## Users

### Auth Solana User

    - Method: GET
    - Path: /users
    - Summary: Authorize Solana user.

**Request**

Path Parameters:

```
wallet_address:str
```

**Response**

Supported Media Types:

- `application/json`

**Response Status Codes**

- 200 Response: The user was successfully authorized.
- 400 Response: Bad request syntax or unsuported method.

**Examples**

Request Header:

```
X-API-Key: 0ef3c43d-a3ac-52a1-938b-57cff7e60282
```

Request Parameter:

```
/users/9ZNTfG4NyQgxy2SWjSiQoUyBPEvXT2xo7fKc5hPYYJ7b
```

HTTP Status Code:

```
200
```

JSON Response:

```json
{
  "wallet_address": "9ZNTfG4NyQgxy2SWjSiQoUyBPEvXT2xo7fKc5hPYYJ7b",
  "api_key": "e8e5725b-7f33-5bad-9438-e63bdbd2efea",
  "user_id": "5ca167d6-1654-11ed-908f-00155d3ecff4"
}
```
