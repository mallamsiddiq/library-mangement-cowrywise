### [pLeAse ReAd ME !]

# Library Management System API API

## Overview
This project is a library management system with separate APIs for frontend and backend administration. It allows users to borrow books, view available books, and enables administrators to manage the book catalogue and track user activities.

### Features
### Frontend [library users] API
- Enroll Users: Add new users to the library.
- List Available Books: Retrieve a list of books currently available in the library.
- Get Book by ID: Retrieve details of a specific book.
- Filter Books: Filter books by publisher and category.
- Borrow Books: Borrow a book by specifying the duration (in days).
### Features
### Frontend [library users] API
- Enroll Users: Add new users to the library.
- List Available Books: Retrieve a list of books currently available in the library.
- Get Book by ID: Retrieve details of a specific book.
- Filter Books: Filter books by publisher and category.
- Borrow Books: Borrow a book by specifying the duration (in days).
### Backend/Admin API
- Add Books: Add new books to the library catalogue.
- Remove Books: Remove books from the library catalogue.
- List Users: Fetch a list of all users enrolled in the library.
- User Borrowed Books: Fetch a list of books borrowed by a specific user.
- Unavailable Books: List books that are currently not available for borrowing, including their expected return date.

- Add Books: Add new books to the library catalogue.
- Remove Books: Remove books from the library catalogue.
- List Users: Fetch a list of all users enrolled in the library.
- User Borrowed Books: Fetch a list of books borrowed by a specific user.
- Unavailable Books: List books that are currently not available for borrowing, including their expected return date.


## Technologies Used

**Django**, **Django REST Framework (DRF)**, **PostgreSQL**, **Docker**, **RabbitMQ**, **Python**

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
10. [Scope and Limitations](#Scope-and-Limitations)
11. [Copyright](#copyright)

## Setup
## Technologies Used

**Django**, **Django REST Framework (DRF)**, **PostgreSQL**, **Docker**, **RabbitMQ**, **Python**

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
10. [Scope and Limitations](#Scope-and-Limitations)
11. [Copyright](#copyright)

## Setup

### Prerequisites

- Docker
- Docker Compose

### Installation
### Installation

1. **Clone the repository:**
1. **Clone the repository:**

    ```bash
    git clone https://github.com/mallamsiddiq/library-mangement-cowrywise .
    ```
    ```bash
    git clone https://github.com/mallamsiddiq/library-mangement-cowrywise .
    ```

2. **Build and run the Docker containers:**
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

- - Or use the make command, I added make.bat if you are on windows and makefile if you are not 

- **Spin Up the Docker Containers:**
   ```sh
   make start
   ```
- **Stop Docker Containers:**
   ```sh
   make stop
   ```
- **View Docker Logs:**
   ```sh
   make logs
   ```
- **Run Tests:**
   ```sh
   make test-all
   ```

3. **Access the services:**
    frontend api is hosted on port 9090
    admin api is hosted on port 8080
    - **Frontend:** [http://localhost:9090](http://localhost:9090)
    - **Admin API:** [http://localhost:8080](http://localhost:8080)

**Documentation is Accesible on:**
- http://localhost:8080/api/v1/doc/
- http://localhost:9090/api/v1/doc/


## Authentication

### User Authentication

http://localhost:8080/api/v1/doc/

- **Register a User:**
  
  `POST /auth/register/`
  
    ```bash
    # For the admin service
    # cd into the admin root to spin
    cd admin
    # run
    docker compose up -d --build

    # For the users service
    # (on another terminal:preferably) also cd into the users ro
    cd ../users
    # run
    docker compose up -d --build
    ```

- - Or use the make command, I added make.bat if you are on windows and makefile if you are not 

- **Spin Up the Docker Containers:**
   ```sh
   make start
   ```
- **Stop Docker Containers:**
   ```sh
   make stop
   ```
- **View Docker Logs:**
   ```sh
   make logs
   ```
- **Run Tests:**
   ```sh
   make test-all
   ```

3. **Access the services:**
    frontend api is hosted on port 9090
    admin api is hosted on port 8080
    - **Frontend:** [http://localhost:9090](http://localhost:9090)
    - **Admin API:** [http://localhost:8080](http://localhost:8080)

**Documentation is Accesible on:**
- http://localhost:8080/api/v1/doc/
- http://localhost:9090/api/v1/doc/


## Authentication

### User Authentication

http://localhost:8080/api/v1/doc/

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
    "firstname": "John",
    "id": "your uuid",
    "lastname": "Doe",
    "email": "john.doe@example.com",
  }
  ```
    "firstname": "John",
    "lastname": "Doe",
    "email": "john.doe@example.com",
    "password": "yourpassword"
  }
  ```

  **Response:**
  
  ```json
  {
    "firstname": "John",
    "id": "your uuid",
    "lastname": "Doe",
    "email": "john.doe@example.com",
  }
  ```

- **Login:**
  
  `POST /auth/login/`
  
- **Login:**
  
  `POST /auth/login/`
  
  **Request Body:**
  
  
  ```json
  {
    "email": "john.doe@example.com",
    "password": "yourpassword"
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
    "detail": "User registered successfully",
    "firstname": "Admin",
    "lastname": "User",
    "email": "admin@cowrywise.com",
  }
  ```

- **Admin Login:**
  
  `POST /auth/login/`
  
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
    "detail": "User registered successfully",
    "firstname": "Admin",
    "lastname": "User",
    "email": "admin@cowrywise.com",
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

#### `POST /library/books/{book_id}/borrow/`
Creates a new book borrow issuance .

**Request Body:**

```json
{
  "date_to_return": "YYYY-MM-DDTHH:MM:SSZ",
  "user": "your id", "optional, you can ignore if you have auth token,  the system knows you if you are logged in"
}
```

#### `GET /library/borrowing/{id}/`
Retrieves details of a specific borrowing issuance.

## Usage Examples

### Example Request: List Unavailable Books

```bash
curl -H "Authorization: Bearer your-access-token" http://localhost:8080/library/books/unavailables/
```

### Example Request: Borrowed Books by User

```bash
curl -H "Authorization: Bearer your-access-token" http://localhost:8080/library/books/borrowed-by_user/123e4567-e89b-12d3-a456-426614174000/


```

- **Django Admin Dashboard:**
  `/admin/`
#### `GET /library/books/{id}/`
Retrieves details of a specific book.

#### `DELETE /library/books/{id}/`
Deletes a specific book (admin only).

#### `GET /library/users/`
Lists all users (admin only).

#### `GET /library/borrowing/`
Lists all issuances (admin only).
this endpoint list issuances with corresponding users and books

#### `POST /library/books/{book_id}/borrow/`
Creates a new book borrow issuance .

**Request Body:**

```json
{
  "return_in_days": "<int>",
  "user": "your id", "optional, you can ignore if you have auth token,  the system knows you if you are logged in"
}
```

#### `GET /library/borrowing/{id}/`
Retrieves details of a specific borrowing issuance.

## Usage Examples

### Example Request: List Unavailable Books

```bash
curl -H "Authorization: Bearer your-access-token" http://localhost:8080/library/books/unavailables/
```

### Example Request: Borrowed Books by User

```bash
curl -H "Authorization: Bearer your-access-token" http://localhost:8080/library/books/borrowed-by_user/123e4567-e89b-12d3-a456-426614174000/


```

- **Django Admin Dashboard:**
  `/admin/`

## Testing

I have created comprenhensive tests for the two services, availabe at app/tests for each services, it covers edge all cases

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
or user the make file provided
I have created comprenhensive tests for the two services, availabe at app/tests for each services, it covers edge all cases

To run tests, ensure Docker containers are running and execute:

Navigate to the respective directories and build the containers:

```bash
# For the admin service
cd admin
docker-compose exec api python manage.py test

# For the users service
cd ../users
docker-compose exec api python manage.py test
```
or user the make file provided

```bash
  make test_users
  make test_admin
  make test_all
```


## Scope and Limitations

- **Efficient Querying and Filtering:** To enhance efficiency in querying and filtering operations, especialy in retrieving complex queries, the `copies_borrowed` field was added to the **Book** table. This field tracks the number of book coppies borrowed is auto incremented when a book is borrowed or returned respecfuly

- **Publisher and Made Enums Real:** The `publisher` field, along with other relevant fields, has been set up with enumerations for stricter validation and consistency in the data.

- **No Borrowing Duplicate Copies:** A user cannot borrow the same book twice without returning the earlier borrowed copy first. This ensures that users do not have duplicate active borrowings of the same title.

- **Unavailable Books:** Users are restricted from borrowing books that are marked as unavailable in the catalogue. The system automatically prevents requests for books that are either checked out or have no available copies left.


## Security Concerns and Limitations

- **Public `.env` Variables:** The `.env` file has been made public in the repository to simplify the setup and configuration process. This is only recommended for local development and testing environments. Ensure the `.env` file is secured and excluded in production.

- **Unauthenticated Endpoints:** Some admin endpoints are currently unauthenticated for ease of setup and usage (to play with). This configuration is not suitable for production environments. Also Endpoints on the users side trequires the user Identity are made flexible, login or provide your user uuid.

## Copyright

© [2024 Akinyemi Sodiq].

For inquiries, please contact:

- **Developer:** mallamsiddiq@gmail.com
  make test_users
  make test_admin
  make test_all
```


## Scope and Limitations

- **Efficient Querying and Filtering:** To enhance efficiency in querying and filtering operations, especialy in retrieving complex queries, the `copies_borrowed` field was added to the **Book** table. This field tracks the number of book coppies borrowed is auto incremented when a book is borrowed or returned respecfuly

- **Publisher and Made Enums Real:** The `publisher` field, along with other relevant fields, has been set up with enumerations for stricter validation and consistency in the data.

- **No Borrowing Duplicate Copies:** A user cannot borrow the same book twice without returning the earlier borrowed copy first. This ensures that users do not have duplicate active borrowings of the same title.

- **Unavailable Books:** Users are restricted from borrowing books that are marked as unavailable in the catalogue. The system automatically prevents requests for books that are either checked out or have no available copies left.


## Security Concerns and Limitations

- **Public `.env` Variables:** The `.env` file has been made public in the repository to simplify the setup and configuration process. This is only recommended for local development and testing environments. Ensure the `.env` file is secured and excluded in production.

- **Unauthenticated Endpoints:** Some admin endpoints are currently unauthenticated for ease of setup and usage (to play with). This configuration is not suitable for production environments. Also Endpoints on the users side trequires the user Identity are made flexible, login or provide your user uuid.

## Copyright

© [2024 Akinyemi Sodiq].

For inquiries, please contact:

- **Developer:** mallamsiddiq@gmail.com
