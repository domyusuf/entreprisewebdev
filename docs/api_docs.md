# API Documentation

All endpoints are protected with Basic Authentication.

- **Username:** `admin`
- **Password:** `password`

## Endpoints

### `GET /transactions`

- **Description:** Retrieves a list of all transactions.
- **Request:**

  ```bash
  curl http://localhost:8000/transactions -u admin:password
  ```

- **Response:** `200 OK`

  ```json
  [
    {
      "id": 0,
      "protocol": "0",
      "address": "M-Money",
      "date": "1715351506754",
      "type": "1",
      "subject": "null",
      "body": "...",
      "toa": "null",
      "sc_toa": "null",
      "service_center": "+250788110381",
      "read": "1",
      "status": "-1",
      "locked": "0",
      "date_sent": "1715351498000",
      "sub_id": "6",
      "readable_date": "10 May 2024 4:31:46 PM",
      "contact_name": "(Unknown)"
    },
    ...
  ]
  ```

### `GET /transactions/{id}`

- **Description:** Retrieves a single transaction by its ID.
- **Request:**

  ```bash
  curl http://localhost:8000/transactions/1 -u admin:password
  ```

- **Response:** `200 OK`

  ```json
  {
    "id": 1,
    "protocol": "0",
    "address": "M-Money",
    "date": "1715351506754",
    "type": "1",
    "subject": "null",
    "body": "...",
    "toa": "null",
    "sc_toa": "null",
    "service_center": "+250788110381",
    "read": "1",
    "status": "-1",
    "locked": "0",
    "date_sent": "1715351498000",
    "sub_id": "6",
    "readable_date": "10 May 2024 4:31:46 PM",
    "contact_name": "(Unknown)"
  }
  ```

- **Error Response:** `404 Not Found` if the transaction ID does not exist.

### `POST /transactions`

- **Description:** Creates a new transaction.
- **Request:**

  ```bash
  curl -X POST http://localhost:8000/transactions \
  -u admin:password \
  -H "Content-Type: application/json" \
  -d '{ "protocol": "0", "address": "New-Address", ... }'
  ```

- **Response:** `201 Created`

  ```json
  {
    "id": 1691,
    "protocol": "0",
    "address": "New-Address",
    ...
  }
  ```

### `PUT /transactions/{id}`

- **Description:** Updates an existing transaction.
- **Request:**

  ```bash
  curl -X PUT http://localhost:8000/transactions/1691 \
  -u admin:password \
  -H "Content-Type: application/json" \
  -d '{ "body": "This is an updated transaction." }'
  ```

- **Response:** `200 OK`

  ```json
  {
    "id": 1691,
    "protocol": "0",
    "address": "New-Address",
    "body": "This is an updated transaction.",
    ...
  }
  ```

- **Error Response:** `404 Not Found` if the transaction ID does not exist.

### `DELETE /transactions/{id}`

- **Description:** Deletes a transaction by its ID.
- **Request:**

  ```bash
  curl -X DELETE http://localhost:8000/transactions/1691 -u admin:password
  ```

- **Response:** `204 No Content`
- **Error Response:** `404 Not Found` if the transaction ID does not exist.

### `GET /search-comparison`

- **Description:** Compares the performance of linear search and dictionary lookup for finding transactions.
- **Request:**

  ```bash
  curl http://localhost:8000/search-comparison -u admin:password
  ```

- **Response:** `200 OK`

  ```json
  {
    "linear_search_avg_time": 1.71661376953125e-06,
    "dictionary_lookup_avg_time": 4.5299530029296873e-07
  }
  ```

### Error Codes

- `400 Bad Request`: Invalid request, e.g., invalid transaction ID.
- `401 Unauthorized`: Missing or invalid authentication credentials.
- `404 Not Found`: The requested resource could not be found.
