Here's the updated README with a copyright section and contact information:

---

# Library Management System API

This project provides a RESTful API for managing a library system, including user authentication, book management, and issuance tracking.

## Table of Contents

1. [Setup](#setup)
2. [Authentication](#authentication)
3. [API Endpoints](#api-endpoints)
4. [Usage Examples](#usage-examples)
5. [Testing](#testing)
6. [Docker Setup](#docker-setup)
7. [Security Concerns and Limitations](#security-concerns-and-limitations)
8. [Contributing](#contributing)
9. [License](#license)
10. [Copyright](#copyright)

## Setup

### Prerequisites

- Docker
- Docker Compose

### Installation

1. **Clone the repository:**

    ```bash
    git clone https://github.com/mallamsiddiq/library-mangement-cowrywise .
    ```

2. **Build and run the Docker containers:**

    ```bash
    # For the admin service
    # cd into the admin root to spin
    cd cowrywise/admin
    # run
    docker compose up -d --build

    # For the users service
    # (on another terminal:preferably) also cd into the users ro
    cd ../users
    # run
    docker compose up -d --build
    ```

3. **Access the services:**
    frontend api is hosted on port 9090
    admin api is hosted on port 8080
    - **Frontend:** [http://localhost:9090](http://localhost:9090)
    - **Admin API:** [http://localhost:8080](http://localhost:8080)

## Authentication

### User Authentication

- **Register a User:**
  
  `POST /auth/register/`
  
  **Request Body:**
  
  ```json
  {
    "firstname": "John",
    "lastname": "Doe",
    "email": "john.doe@example.com",
    "password": "yourpassword"
  }
  ```

  **Response:**
  
  ```json
  {
    "detail": "User registered successfully"
  }
  ```

- **Login:**
  
  `POST /auth/login/`
  
  **Request Body:**
  
  ```json
  {
    "email": "john.doe@example.com",
    "password": "yourpassword"
  }
  ```

  **Response:**
  
  ```json
  {
    "access": "your-access-token",
    "refresh": "your-refresh-token"
  }
  ```

### Admin Authentication

- **Admin Registration:**
  
  `POST /auth/admin-signup/`
  
  **Request Body:**

  For simple simulation of admin registery only @cowrywise enail is allowed
  e.g. random-string@cowrywise.com
  
  ```json
  {
    "firstname": "Admin",
    "lastname": "User",
    "email": "admin@cowrywise.com",
    "password": "adminpassword"
  }
  ```

  **Response:**
  
  ```json
  {
    "detail": "User registered successfully"
  }
  ```

- **Admin Login:**
  
  `POST /auth/login/`
  
  **Request Body:**
  
  ```json
  {
    "email": "admin@cowrywise.com",
    "password": "adminpassword"
  }
  ```

  **Response:**
  
  ```json
  {
    "access": "your-access-token",
    "refresh": "your-refresh-token"
  }
  ```

## API Endpoints

### Authentication API

#### `POST /auth/register/`
Registers a new user.

#### `POST /auth/login/`
Logs in a user and returns JWT tokens.

#### `POST /auth/admin-signup/`
Registers a new admin user (must be `@cowrywise.com` domain).

#### `POST /auth/login/`
Logs in an admin user and returns JWT tokens.

#### `GET /auth/me/`
Returns the profile information of the authenticated user.

#### `PATCH /auth/update-me/`
Updates the profile information of the authenticated user.

### Library API

#### `GET /library/books/`
Lists all books.

- **Query Parameters:**
  - `unavailables` – Lists books that are currently unavailable.
  - `borrowed-by_user/{user_id}` – Lists books borrowed by a specific user.

#### `POST /library/books/`
Creates a new book (admin only).

**Request Body:**

```json
{
  "title": "Book Title",
  "author": "Author Name",
  "publisher": "Publisher Name",
  "category": "Category Name",
  "total_copies": 5
}
```

#### `GET /library/books/{id}/`
Retrieves details of a specific book.

#### `DELETE /library/books/{id}/`
Deletes a specific book (admin only).

#### `GET /library/users/`
Lists all users (admin only).

#### `GET /library/borrowing/`
Lists all issuances (admin only).
this endpoint list issuances with corresponding users and books

#### `POST /library/books/{book_id}borrowing/` {protecte identify the user}
Creates a new book borrow issuance .

**Request Body:**

```json
{
  "date_to_return": "YYYY-MM-DDTHH:MM:SSZ"
}
```

#### `GET /library/borrowing/{id}/`
Retrieves details of a specific issuance.

## Usage Examples

### Example Request: List Unavailable Books

```bash
curl -H "Authorization: Bearer your-access-token" http://localhost:8080/library/books/unavailables/
```

### Example Request: Borrowed Books by User

```bash
curl -H "Authorization: Bearer your-access-token" http://localhost:8080/library/books/borrowed-by_user/123e4567-e89b-12d3-a456-426614174000/
```

## Testing

To run tests, ensure Docker containers are running and execute:

Navigate to the respective directories and build the containers:

```bash
# For the admin service
cd cowrywise/admin
docker-compose exec api python manage.py test

# For the users service
cd ../users
docker-compose exec api python manage.py test
```


## Scope and Limitations

- Publisher and made Enums real
- The .env Variables are made public to ease setup set up and  configuration 
- User can't borrow a book twice without return the earlier copy
- You can't borrrow borrow that is unavailable books in the catalogue


## Security Concerns and Limitations

- **Unauthenticated Admin Endpoints:** Some admin endpoints are currently unauthenticated for ease of setup and usage. This configuration is not suitable for production environments. Consider implementing proper authentication and authorization before deploying to production.

- **.env File:** The `.env` file containing sensitive environment variables is available in the repository for ease of setup. This file should not be exposed or committed to version control in production environments. Make sure to secure this file and use appropriate environment variable management practices in production.


## Copyright

© [2024 Akinyemi Sodiq].

For inquiries, please contact:

- **Developer:** mallamsiddiq@gmail.com
