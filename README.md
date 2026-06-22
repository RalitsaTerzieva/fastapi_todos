# FastAPI Todo App with JWT Authentication

A full-stack Todo application built with **FastAPI**, featuring JWT authentication, PostgreSQL integration, and server-side rendered pages using Jinja2 templates.

---

## 🚀 Features

### Authentication
- User registration
- User login with JWT authentication
- Password hashing with bcrypt
- Protected routes and API endpoints
- Authentication using access tokens stored in cookies

### Todo Management
- Create todos
- View personal todo list
- Update existing todos
- Delete todos
- User-specific todo ownership

### Server-Side Rendering
- Login page
- Registration page
- Todo list page
- Add Todo page
- Edit Todo page
- Shared layout and navigation using Jinja2 templates

---

## 🛠 Tech Stack

### Backend
- FastAPI
- SQLAlchemy
- PostgreSQL
- Alembic
- Uvicorn

### Authentication & Security
- Passlib (bcrypt password hashing)
- Python-JOSE (JWT token generation and validation)
- OAuth2 Password Bearer

### Frontend
- Jinja2 Templates
- HTML5
- Bootstrap
- JavaScript (Fetch API)

---

## 📂 Application Pages

| Page | Description |
|--------|-------------|
| Login | Authenticate existing users |
| Register | Create a new account |
| Todo List | View all todos belonging to the logged-in user |
| Add Todo | Create a new todo |
| Edit Todo | Update or delete an existing todo |

---

## 🔒 Security

- Passwords are hashed before storage
- JWT tokens are used for authentication
- Protected routes require a valid authenticated user
- Users can only access and manage their own todos

---

## 📦 Database

The application uses PostgreSQL with SQLAlchemy ORM and Alembic migrations.

### User Model

- Username
- Email
- First Name
- Last Name
- Phone Number
- Role
- Hashed Password

### Todo Model

- Title
- Description
- Priority
- Completion Status
- Owner ID

---

## ▶️ Running the Project

Start the development server:

```bash
uvicorn main:app --reload