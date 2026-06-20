# Library Management System API

A RESTful Library Management System built using FastAPI, PostgreSQL, SQLAlchemy, and Pydantic.

This project is being developed to learn backend development concepts such as:

* FastAPI
* PostgreSQL
* SQLAlchemy ORM
* Pydantic Validation
* REST APIs
* Database Relationships
* Business Logic Implementation

---

## Features

### Author Management

* Create Author
* View Authors
* Update Author
* Delete Author

### Category Management

* Create Category
* View Categories
* Update Category
* Delete Category

### Book Management

* Create Book
* View Books
* Update Book
* Delete Book

### Borrow Management

* Borrow a Book
* Return a Book
* View Borrow Records

---

## Tech Stack

| Technology | Purpose           |
| ---------- | ----------------- |
| FastAPI    | Backend Framework |
| PostgreSQL | Database          |
| SQLAlchemy | ORM               |
| Pydantic   | Data Validation   |
| Uvicorn    | ASGI Server       |

---

## Project Structure

```text
library_management_fastapi/
│
├── app/
│   ├── models/
│   ├── schemas/
│   ├── routers/
│   ├── database.py
│   └── main.py
│
├── .env.example
├── .gitignore
├── README.md
└── requirements.txt
```

---

## Database Schema

### Author

```text
id
name
email
```

### Category

```text
id
name
```

### Book

```text
id
title
isbn
publication_year
total_copies
available_copies
author_id
category_id
```

### Borrow Record

```text
id
book_id
borrower_name
issue_date
return_date
status
```

---

## Installation

### Clone Repository

```bash
git clone <repository-url>
cd library_management_fastapi
```

### Create Virtual Environment

```bash
python -m venv myenv
```

### Activate Virtual Environment

Windows:

```bash
myenv\Scripts\activate
```

Linux/Mac:

```bash
source myenv/bin/activate
```

### Install Dependencies

```bash
pip install -r requirements.txt
```

---

## Environment Variables

Create a `.env` file in the root directory.

```env
DATABASE_URL=postgresql://username:password@localhost:5432/<database_name>
```

---

## Run the Application

```bash
uvicorn app.main:app --reload
```

Application URL:

```text
http://127.0.0.1:8000
```

Swagger Documentation:

```text
http://127.0.0.1:8000/docs
```

ReDoc Documentation:

```text
http://127.0.0.1:8000/redoc
```

---

## Future Enhancements

* JWT Authentication
* Role-Based Access Control
* Alembic Migrations
* Pagination
* Search and Filtering
* Docker Support
* Unit Testing

---

## Learning Objectives

This project is intended to provide hands-on experience with:

* REST API Development
* Database Design
* SQLAlchemy Relationships
* FastAPI Dependency Injection
* Pydantic Models
* Backend Project Structure