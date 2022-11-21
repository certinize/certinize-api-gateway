# Common

## Certificates

### Generate eCertificate

```properties
- Method: POST
- Path: /certificates
- Summary: Generate an e-Certificate.
```

**Request**\
Supported Media Types:

```properties
application/json
```

**Response**\
Supported Media Types:

```properties
application/json
```

**Response Status Codes**\
Status:

```sh
201 Response: The e-Certificate(s) was created.
400 Response: Bad request syntax or unsupported method.
```

**Examples**\
Request Header:

```properties
X-API-Key: 0ef3c43d-a3ac-52a1-938b-57cff7e60282
```

Request Body:

```json
{
  "template_config_id": "36b91a30-16fb-11ed-8a9e-00155d3ecff4",
  "issuance_date": "2022-01-31",
  "recipients": [
    {
      "recipient_name": "Juan Cruz"
    }
  ]
}
```

HTTP Status Code:

```sh
201
```

JSON Response:

```json
{
  "certificate": [
    {
      "certificate_url": "https://...",
      "file_id": "1k-UTikDkXmQomW28VYpWhQDgu2ced0uU",
      "recipient_name": "Juan Cruz",
      "issuance_date": "2022-01-30"
    }
  ],
  "certificate_id": "36b91a30-16fb-11ed-8a9e-00155d3ecff4",
  "template_config_id": "e46286c6-2136-11ed-b1e8-00155d886c22"
}
```

### Get Certificate

```properties
- Method: GET
- Path: /certificates/{certificate_id:uuid}
- Summary: Get a specific certificate.
```

**Request**\
Path Parameters:

```properties
certificate_id:uuid
```

**Response**\
Supported Media Types:

```properties
application/json
```

**Response Status Codes**\
Status:

```sh
200 Response: The request was fulfilled.
400 Response: Bad request syntax or unsupported method.
```

**Examples**\
Request Header:

```properties
X-API-Key: 0ef3c43d-a3ac-52a1-938b-57cff7e60282
```

Request Parameter:

```sh
/configurations/36b91a30-16fb-11ed-8a9e-00155d3ecff4
```

HTTP Status Code:

```sh
200
```

JSON Response:

```json
{
  "certificate_id": "36b91a30-16fb-11ed-8a9e-00155d3ecff4",
  "template_config_id": "e46286c6-2136-11ed-b1e8-00155d886c22",
  "certificate": {
      "certificate": [
          {
              "certificate_url": "https://...",
              "file_id": "1k-UTikDkXmQomW28VYpWhQDgu2ced0uU",
              "recipient_name": "Juan Cruz",
              "issuance_date": "2022-01-30"
          }
      ]
  }
}
```

## Configurations

### Create Template Configuration

```properties
- Method: POST
- Path: /configurations
- Summary: Save an e-Certificate template configuration.
```

**Request**\
Supported Media Types:

- `application/json`

**Response**\
Supported Media Types:

- `application/json`

**Response Status Codes**\
Status:

```sh
201 Response: The e-Certificate template configuration was created.
400 Response: Bad request syntax or unsupported method.
```

**Examples**\
Request Header:

```properties
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

```sh
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

```properties
- Method: GET
- Path: /configurations/{template_config_id:uuid}
- Summary: Get a specific template configuration.
```

**Request**\
Path Parameters:

```properties
template_config_id:uuid
```

**Response**\
Supported Media Types:

```properties
application/json
```

**Response Status Codes**\
Status:

```sh
200 Response: The request was fulfilled.
400 Response: Bad request syntax or unsupported method.
```

**Examples**\
Request Header:

```properties
X-API-Key: 0ef3c43d-a3ac-52a1-938b-57cff7e60282
```

Request Parameter:

```sh
/configurations/6e9fd408-207d-11ed-9d54-00155d886c22
```

HTTP Status Code:

```sh
200
```

JSON Response:

```json
{
  "font": {
    "font_url": "https://example.com/FontFile.ttf",
    "font_id": "e632f180-2056-11ed-b912-bb65d3909f61"
  },
  "template": {
    "template_path": "/certinize-bucket/cdbcfa87-2136-11ed-bf4e-00155d886c22_WROGguGnZ",
    "template_id": "cf8138ce-2136-11ed-9a61-00155d886c22",
    "template_height": 720,
    "template_size": 97583,
    "template_url": "https://example.com/template.jpeg",
    "template_width": 1040,
    "template_name": "cdbcfa87-2136-11ed-bf4e-00155d886c22_WROGguGnZ",
    "template_thumbnail_url": "https://example.com/template-thumbnail.jpeg"
  },
  "template_config": {
    "template_config_id": "6e9fd408-207d-11ed-9d54-00155d886c22",
    "template_config_name": "my template",
    "template_id": "cf8138ce-2136-11ed-9a61-00155d886c22",
    "font_id": "e632f180-2056-11ed-b912-bb65d3909f61",
    "config_meta": {
      "recipient_name_meta": {
        "position": {
          "x": 960,
          "y": 540
        },
        "font_size": 24
      },
    }
  }
}
```

### List Template Configurations

```properties
- Method: GET
- Path: /configurations
- Summary: Get a list of template configurations.
```

**Request**\
There are no request parameters for this operation.

**Response**\
Supported Media Types:

```properties
application/json
```

**Response Status Codes**\
Status:

```sh
200 Response: The request was fulfilled.
400 Response: Bad request syntax or unsupported method.
```

**Examples**\
Request Header:

```properties
X-API-Key: 0ef3c43d-a3ac-52a1-938b-57cff7e60282
```

Request Path:

```properties
/configurations
```

HTTP Status Code:

```sh
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
        "font_url": "https://example.com/FontFile.ttf"
      },
      "template": {
        "template_height": 720,
        "template_id": "89b22a51-2057-11ed-9d28-00155d886c22",
        "template_name": "template_name",
        "template_path": "/certinize-bucket/template_name",
        "template_size": 97583,
        "template_thumbnail_url": "https://example.com/template-thumbnail.jpeg",
        "template_url": "https://example.com/template.jpeg",
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

```properties
- Method: GET
- Path: /fonts
- Summary: Retrieve all usable e-Certificate fonts.
```

**Request**\
There are no request parameters for this operation.

**Response**\
Supported Media Types:

```properties
application/json
```

**Response Status Codes**\
Status:

```sh
200 Response: The request was fulfilled.
400 Response: Bad request syntax or unsupported method.
```

**Examples**\
Request Header:

```properties
X-API-Key: 0ef3c43d-a3ac-52a1-938b-57cff7e60282
```

Request Path:

```properties
/fonts
```

HTTP Status Code:

```sh
200
```

JSON Response:

```json
{
  "fonts": [
    {
      "font_id": "8082c1c8-1e33-11ed-b68e-8bb3135194ad",
      "font_url": "https://example.com/FontFile.ttf"
    },
    ...
  ]
}
```

## Issuances

### Transfer Certificate

```properties
- Method: POST
- Path: /issuances
- Summary: Transfer an e-Certificate to a recipient(s).
- Description: Transfer generated e-Certificate(s) inside an e-Certificate collection. The recipient(s) should be listed in the collection metadata.
```

**Request**\
Supported Media Types:

```properties
application/json
```

**Response**\
Supported Media Types:

```properties
application/json
```

**Response Status Codes**\
Status:

```sh
202 Response: E-Certificate issuance request accepted.
400 Response: Bad request syntax or unsupported method.
```

**Examples**\
Request Header:

```properties
X-API-Key: 0ef3c43d-a3ac-52a1-938b-57cff7e60282
```

Request Body:

> The issuer_id is used to check if the issuer is a verified user.

```json
{
  "issuer_meta": {
    "issuer_id": "144b084c-374e-11ed-8e58-d7cfa0c850a6",
    "issuer_name": "Issuer Name",
    "issuer_email": "issuer@example.com",
    "issuer_website": "https://issuer-website.com",
    "issuer_pubkey": "ZaXGjYvxgVTemk9Rx42hw9zBAjPjH3r41Aqy9xuQRrL1",
    "issuer_pvtket": "9Hb2TDTMB8wfRNg7g6EPdZbkzRLYw2WGSvVYNoc8m9jrF63uGpTsHPBVyWDhPBrDaevftJUDRmVLad9TgAJT9GZJ"
  },
  "recipient_meta": [
    {
      "recipient_email": "recipient@example.com",
      "recipient_name": "Juan dela Cruz",
      "recipient_pubkey": "B7KNk9UWUGjg89NrmuCvuzNc9dNrmQYCQtcQB525a8HU",
      "recipient_ecert_url": "https://storage.com/certificate.jpeg"
    }
  ]
}
```

HTTP Status Code:

```sh
202
```

JSON Response:

```json
{
  "message": "Issuance request accepted"
}
```

## Templates

### Add eCertificate Template

```properties
- Method: POST
- Path: /templates
- Summary: Upload an e-Certificate template(s).
```

**Request**\
Supported Media Types:

```properties
application/json
```

**Response**\
Supported Media Types:

```properties
application/json
```

**Response Status Codes**\
Status:

```sh
201 Response: The e-Certificate template(s) was uploaded.
400 Response: Bad request syntax or unsupported method.
```

**Examples**\
Request Header:

```properties
X-API-Key: 0ef3c43d-a3ac-52a1-938b-57cff7e60282
```

Form Data:

```json
{
  "templates": [
    "data:image/jpeg;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAQAAAC1HAwCAAAAC0lEQVQYV2NgYAAAAAMAAWgmWQ0AAAAASUVORK5CYII="
  ]
}
```

HTTP Status Code:

```sh
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
  "template_thumbnail_url": "https://example.com/template-thumbnail.jpeg",
  "template_url": "https://example.com/template.jpeg",
  "template_width": 773
}
```

For multiple file uploads, the response will contain a list of template metadata:

```json
{
  "templates": [
    {
      "template_id": "1a62a09e-1a46-11ed-b3e0-00155d3fe822",
      "template_url": "https://example.com/template.jpeg",
      ...
    },
    ...
  ]
}
```

### List Templates

```properties
- Method: GET
- Path: /templates
- Summary: Get a list of e-Certificate templates.
- Description: This will list all recorded e-Certificate templates.
```

**Request**\
There are no request parameters for this operation.

Supported Media Types:

```properties
application/json
```

**Response Status Codes**\
Status:

```sh
200 Response: The request was fulfilled.
400 Response: Bad request syntax or unsupported method.
```

**Examples**\
Request Header:

```properties
X-API-Key: 0ef3c43d-a3ac-52a1-938b-57cff7e60282
```

Request Parameter:

```sh
/templates
```

HTTP Status Code:

```sh
200
```

JSON Response:

```json
{
  "templates": [
    {
      "template_id": "e82fbcd5-3f45-483e-887b-5ffec0194c42",
      "template_url": "https://example.com/template.jpeg"
    }
  ]
}
```

## Users

### Auth User

```properties
- Method: GET
- Path: /users
- Summary: Authorize and authenticate user.
```

**Request**\
Path Parameters:

```properties
wallet_address:str
```

**Response**\
Supported Media Types:

```properties
application/json
```

**Response Status Codes**\
Status:

```sh
200 Response: The user was successfully authorized.
400 Response: Bad request syntax or unsupported method.
```

**Examples**\
Request Header:

```properties
X-API-Key: 0ef3c43d-a3ac-52a1-938b-57cff7e60282
```

Request Parameter:

```sh
/users/9ZNTfG4NyQgxy2SWjSiQoUyBPEvXT2xo7fKc5hPYYJ7b
```

HTTP Status Code:

```sh
200
```

JSON Response:

```json
{
  "name": "Juan Cruz",
  "website": "https://example.com",
  "wallet_address": "9ZNTfG4NyQgxy2SWjSiQoUyBPEvXT2xo7fKc5hPYYJ7b",
  "api_key": "e8e5725b-7f33-5bad-9438-e63bdbd2efea",
  "user_id": "5ca167d6-1654-11ed-908f-00155d3ecff4",
  "is_verified": true
}
```

### Verify User

```properties
- Method: POST
- Path: /users
- Summary: Request for user to be verified.
```

**Request**\
Supported Media Types:

```properties
application/json
```

**Response**\
Supported Media Types:

```properties
application/json
```

**Response Status Codes**\
Status:

```sh
201 Response: The verification request was delivered.
400 Response: Bad request syntax or unsupported method.
```

**Examples**\
Request Header:

```properties
X-API-Key: 0ef3c43d-a3ac-52a1-938b-57cff7e60282
```

Request Body:

```json
{
  "pubkey": "B7KNk9UWUGjg89NrmuCvuzNc9dNrmQYCQtcQB525a8HU",
  "info_link": "https://trends.google.com/trends/explore?q=mseuf&geo=PH",
  "official_website": "https://mseuf.edu.ph/",
  "official_email": "ictd@mseuf.edu.ph",
  "organization_id": "data:image/jpeg;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAQAAAC1HAwCAAAAC0lEQVQYV2NgYAAAAAMAAWgmWQ0AAAAASUVORK5CYII=",
  "approved": false
}
```

HTTP Status Code:

```sh
201
```

JSON Response:

```json
{
  "pubkey": "B7KNk9UWUGjg89NrmuCvuzNc9dNrmQYCQtcQB525a8HU",
  "info_link": "https://trends.google.com/trends/explore?q=mseuf&geo=PH",
  "official_website": "https://mseuf.edu.ph/",
  "official_email": "ictd@mseuf.edu.ph",
  "organization_id": "data:image/jpeg;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAQAAAC1HAwCAAAAC0lEQVQYV2NgYAAAAAMAAWgmWQ0AAAAASUVORK5CYII=",
  "approved": false
}
```
