# Lunch Voting API

## 📌 Project Overview
This API allows company employees to vote for lunch menus from different restaurants. Each restaurant uploads its daily menu, and employees vote before leaving for lunch. The backend supports different versions of the mobile app, ensuring compatibility with older clients.

## 🚀 Features
- **User Authentication** (Registration, Login, Logout, JWT Tokens)
- **Restaurant Management** (Create, Update, Delete, Assign Employees)
- **Menu Management** (Upload and Retrieve Daily Menus)
- **Voting System** (Employees Vote for Menus)
- **Results Calculation** (Get Daily Voting Results)
- **Backward Compatibility** (Supports Different Mobile App Versions)

## 🛠 Tech Stack
- **Django 5 + Django REST Framework** (Backend API)
- **PostgreSQL** (Database)
- **JWT Authentication** (User Authentication & Authorization)
- **Docker & Docker Compose** (Containerization & Deployment)
- **Pytest** (Unit Testing & Integration Testing)
- **Flake8** (Code Linting)

---

## 🏗 Installation & Setup

### 1️⃣ Clone the Repository
```sh
$ git clone https://github.com/your-repo/lunch-voting-api.git
$ cd lunch-voting-api
```

### 2️⃣ Create and Configure Environment Variables
Create a `.env` file in the project root and add the following environment variables:
```ini
# Django Secret Key
SECRET_KEY=your-secret-key

# Debug mode
DEBUG=True

# Database settings
DB_NAME=postgres
DB_USER=postgres
DB_PASSWORD=your-password
DB_HOST=db  # For Docker
DB_PORT=5432

# Allowed Hosts
ALLOWED_HOSTS=127.0.0.1,localhost
```

### 3️⃣ Run the Project using Docker
```sh
$ docker-compose up --build
```

This will start:
- **PostgreSQL Database**
- **Django API Server**

### 4️⃣ Apply Migrations and Create a Superuser
```sh
$ docker exec -it lunch-voting-api-web-1 bash  # Enter the container
$ python manage.py migrate
$ python manage.py createsuperuser  # Follow prompts to create an admin user
```

---

## 📖 API Endpoints

### 🔑 Authentication
| Method | Endpoint | Description |
|--------|---------|-------------|
| `POST` | `/api/auth/register/` | Register a new user |
| `POST` | `/api/auth/login/` | Login and receive JWT tokens |
| `POST` | `/api/auth/logout/` | Logout and blacklist refresh token |
| `GET` | `/api/auth/profile/` | Get authenticated user profile |

### 🍽 Restaurant Management
| Method | Endpoint | Description |
|--------|---------|-------------|
| `GET` | `/api/restaurants/` | Get all restaurants |
| `POST` | `/api/restaurants/` | Create a new restaurant (Admin only) |
| `GET` | `/api/restaurants/{id}/` | Get restaurant details |
| `PATCH` | `/api/restaurants/{id}/` | Update restaurant (Owner only) |
| `DELETE` | `/api/restaurants/{id}/` | Delete restaurant (Owner only) |
| `PATCH` | `/api/restaurants/{id}/add-employee/` | Add an employee to a restaurant |

### 📋 Menu Management
| Method | Endpoint | Description |
|--------|---------|-------------|
| `GET` | `/api/restaurants/{restaurant_id}/menus/` | Get all menus of a restaurant |
| `POST` | `/api/restaurants/{restaurant_id}/menus/` | Upload a new menu (Owner only) |
| `GET` | `/api/restaurants/{restaurant_id}/menus/today/` | Get today's menu |

### 🗳 Voting System
| Method | Endpoint | Description |
|--------|---------|-------------|
| `POST` | `/api/votes/vote/` | Vote for a menu |
| `GET` | `/api/votes/results/` | Get voting results for today |

---


## 🛠 Running Tests
Run all tests using:
```sh
$ pytest
```
Or with coverage report:
```sh
$ pytest --cov
```

---

## 📏 Code Quality Check
Run **Black** to check code style:
```sh
$ black .
```

---




