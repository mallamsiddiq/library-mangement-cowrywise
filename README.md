
# Library Management System

## Overview

This project is a library management system with separate APIs for frontend and backend administration. It allows users to borrow books, view available books, and enables administrators to manage the book catalogue and track user activities.

## Features

### Frontend API

- **Enroll Users**: Add new users to the library.
- **List Available Books**: Retrieve a list of books currently available in the library.
- **Get Book by ID**: Retrieve details of a specific book.
- **Filter Books**: Filter books by publisher and category.
- **Borrow Books**: Borrow a book by specifying the duration (in days).

### Backend/Admin API

- **Add Books**: Add new books to the library catalogue.
- **Remove Books**: Remove books from the library catalogue.
- **List Users**: Fetch a list of all users enrolled in the library.
- **User Borrowed Books**: Fetch a list of books borrowed by a specific user.
- **Unavailable Books**: List books that are currently not available for borrowing, including their expected return date.

## Installation

### Prerequisites

- Python 3.8 or higher
- Docker
- Docker Compose

### Setup

1. **Clone the Repository**

   ```bash
   git clone https://github.com/your-username/library-management-system.git
   cd library-management-system
   ```

2. **Create a Virtual Environment**

   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows use `venv\Scripts\activate`
   ```

3. **Install Dependencies**

   ```bash
   pip install -r requirements.txt
   ```

4. **Run Migrations**

   ```bash
   python manage.py migrate
   ```

5. **Create a Superuser**

   ```bash
   python manage.py createsuperuser
   ```

6. **Run the Development Server**

   ```bash
   python manage.py runserver
   ```

### Docker Setup

To run the application using Docker, follow these steps:

1. **Build and Run Docker Containers**

   ```bash
   docker-compose up --build
   ```

2. **Access the Application**

   Open your browser and navigate to `http://localhost:8000` to access the application.

## Usage

### Frontend API

- **Enroll User**

  POST `/api/users/`

  **Request Body:**

  ```json
  {
      "email": "user@example.com",
      "firstname": "John",
      "lastname": "Doe"
  }
  ```

- **List Available Books**

  GET `/api/books/`

- **Get Book by ID**

  GET `/api/books/{book_id}/`

- **Filter Books**

  GET `/api/books/?publisher=Wiley&category=technology`

- **Borrow Book**

  POST `/api/books/{book_id}/borrow/`

  **Request Body:**

  ```json
  {
      "days": 14
  }
  ```

### Backend/Admin API

- **Add Book**

  POST `/api/admin/books/`

  **Request Body:**

  ```json
  {
      "title": "Example Book",
      "author": "Author Name",
      "publisher": "Wiley",
      "category": "technology",
      "total_copies": 5
  }
  ```

- **Remove Book**

  DELETE `/api/admin/books/{book_id}/`

- **List Users**

  GET `/api/admin/users/`

- **User Borrowed Books**

  GET `/api/admin/users/{user_id}/borrowed-books/`

- **Unavailable Books**

  GET `/api/admin/books/unavailables/`

## Testing

To run tests, use the following command:

```bash
python manage.py test
```

## Contributing

If you want to contribute to this project, please fork the repository and submit a pull request with your changes. 

1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Create a pull request

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
