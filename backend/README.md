# Pharmstock Inventory Management System

Pharmstock is a robust inventory management system designed for pharmacies, built with Django and Django REST Framework. It provides a comprehensive suite of tools to manage medications, track stock levels, handle suppliers, and generate insightful reports.


## Features Implemented

-   **Authentication**: Custom user model with email-based authentication and distinct user roles (Admin, Pharmacist, Staff, Manager).
-   **Inventory Management**: Detailed tracking of medications, including categories, stock levels, batch information with expiration dates, and transaction logging.
-   **Supplier Management**: A complete system for managing supplier information, including contact details and active status.
-   **Reporting**: Generation of key reports such as inventory levels, expiration tracking, and transaction histories.
-   **API**: A well-structured RESTful API with filtering, searching, and pagination for all major features.
-   **Admin Panel**: A comprehensive admin interface for managing all aspects of the system.

## Technologies Used

-   **Backend**:
    -   Python
    -   Django & Django REST Framework
    -   PostgreSQL (or SQLite for development)
-   **API Documentation**:
    -   `drf-yasg` for Swagger/OpenAPI and ReDoc generation.

## Setup and Run Instructions

Follow these steps to get the project up and running on your local machine.

### 1. Prerequisites

-   Python 3.10+
-   Git
-   PostgreSQL (optional, for production-like setup)

### 2. Clone the Repository

```bash
git clone <repository-url>
cd pharmstock-inventory-system/backend
```

### 3. Create and Activate a Virtual Environment

-   **Windows**:
    ```bash
    python -m venv venv
    .\venv\Scripts\activate
    ```
-   **macOS/Linux**:
    ```bash
    python3 -m venv venv
    source venv/bin/activate
    ```

### 4. Install Dependencies

Install all the required packages using pip:

```bash
pip install -r requirements.txt
```

### 5. Configure Environment Variables

Create a `.env` file in the `backend` directory by copying the example file:

```bash
# Example: copy .env.example .env (if you have an example file)
# Or create it manually
```

Add the following environment variables to your `.env` file:

```env
SECRET_KEY='your-secret-key-here'
DEBUG=True
ALLOWED_HOSTS=127.0.0.1,localhost

# Database Configuration (PostgreSQL example)
DB_NAME=pharmstock_db
DB_USER=your_db_user
DB_PASSWORD=your_db_password
DB_HOST=localhost
DB_PORT=5432
```

### 6. Run Database Migrations

Apply the database migrations to create the necessary tables:

```bash
python manage.py migrate
```

### 7. Create a Superuser

Create an admin account to access the Django admin panel:

```bash
python manage.py createsuperuser
```

Follow the prompts to set up your email and password.

### 8. Run the Development Server

Start the Django development server:

```bash
python manage.py runserver
```

The application will be available at `http://127.0.0.1:8000`.

-   **API Root**: `http://127.0.0.1:8000/api/v1/`
-   **Admin Panel**: `http://127.0.0.1:8000/admin/`
-   **API Documentation (Swagger)**: `http://127.0.0.1:8000/swagger/`

## Notes on AI Usage

This project was developed with the assistance of an AI programming agent. The AI was utilized for the following tasks:

-   **Code Generation**: Generating boilerplate code for models, serializers, views, and URLs based on high-level requirements.
-   **Refactoring**: Improving code quality by applying Django and DRF best practices, such as optimizing database queries and structuring serializers.
-   **Implementation**: Wiring up URL patterns, configuring Django settings, and implementing features like filtering and searching in the API.


The AI acted as a pair programmer, accelerating the development process and ensuring adherence to industry-standard conventions.
