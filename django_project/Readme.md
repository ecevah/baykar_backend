# Django UAV Rental System

This project is a web application that offers users UHA (Unmanned Aerial Vehicle) rental services. Developed using Django and PostgreSQL. The application consists of three main tables: IHA, Customer and Reservation.

## Technologies

- Django
- PostgreSQL
- djangorestframework-simplejwt for JWT (JSON Web Token)

## Database Model

- `IHA`: Contains brand, model, weight, hourly price, category and picture.
- `Customer`: It consists of name, surname, username and password.
- `Reservation`: Establishes a many-to-one relationship between the customer and IHA. It includes start and end dates, total price and reservation number.

![ER Diagram](https://github.com/ecevah/baykar_backend/blob/main/django_project/static/er_baykar.png)

## Features

- CRUD operations: Functions that create, delete, update and fetch all parameters for each table.
- Customized queries: Querying based on one or more values in tables with `get_specific` functions.
- Authorization with user login and JWT token.
- Dynamic calculation of the total price in the booking record.

## While starting

### Prerequisites

- Python (3.8 or newer)
- PostgreSQL
- Pipenv or virtualenv (optional)

### Setup

1. Clone the project and go to the project directory.

   ```bash
   git clone https://yourrepository.com/django_iha_kiralama.git
   cd django_iha_kiralama
   ```

2. Install dependencies. (Note: `requirements.txt` file must be added)

   ```bash
   pip install -r requirements.txt
   ```

3. Configure the PostgreSQL database and make the necessary changes in the `settings.py` file.

4. Implement database migrations.

   ```bash
   python manage.py migrate
   ```

5. Start the development server.
   ```bash
   python manage.py runserver
   ```

### API Paths

- `/v1/`: For admin operations.
- `/api/`: For user operations. Access is provided via middleware.

# Django IHA Rental System API Usage

This document provides detailed usage examples for API endpoints of the Django IHA Rental System. The required `Authorization` header for each request and the request body required for POST requests are included. `/v1/` is reserved for admin access only, while `/api/` is designated for client use only.
Detailed API Usage for Reservation App body { font-family: Arial, sans-serif; margin: 20px; } h1 { color: #333; } h2, h3 { color: #555; } p, pre { margin-left: 20px; } pre { background-color: #f4f4f4; padding: 10px; }

# Detailed API Usage for Reservation App

This document provides detailed examples on how to use each API endpoint in the Reservation App, including the required Authorization header and request body for POST requests.

/v1/ is reserved exclusively for admin access, while /api/ is designated solely for customer use.

# API Usage for IHA

## API Endpoints and Usage

### 1\. List IHAs (/api/ihas)

Retrieves a list of all IHAs.

    GET /api/ihas
    Header:
        Authorization: [your_token_here]

**Error Response:**

    {
        "status": false,
        "message": "Error message"
    }

### 2\. Create IHA (/v1/iha/create)

Creates a new IHA. Requires details about the IHA in the request body.

    POST /v1/iha/create
    Header:
        Content-Type: application/json
        Authorization: [your_token_here]
    Body:
        {
            "brand": "IHA Brand",
            "model": "Model",
            "weight": "Weight",
            "category": "Category",
            "price": "Price",
            "image": "Optional image file"
        }

**Successful Response:**

    {
        "status": true,
        "message": "IHA creation successful.",
        "data": {
            "id": "IHA ID",
            "brand": "IHA Brand",
            "model": "Model",
            "weight": "Weight",
            "category": "Category",
            "price": "Price",
            "image_url": "Optional image URL"
        }
    }

**Error Response:**

    {
        "status": false,
        "message": "Error message"
    }

### 3\. Delete IHA (/v1/iha/delete/<iha_id>)

Deletes a specific IHA by ID. Replace <iha_id> with the actual ID of the IHA you want to delete.

    DELETE /v1/iha/delete/[iha_id]
    Header:
        Authorization: [your_token_here]

**Error Response:**

    {
        "status": false,
        "message": "Error message"
    }

### 4\. Update IHA (/v1/iha/update/<iha_id>)

Updates the details of a specific IHA. Provide the new details in the request body.

    PUT /v1/iha/update/[iha_id]
    Header:
        Authorization: [your_token_here]
    Body:
        {
            "name": "New Name",
            "model": "New Model",
            ...
        }

**Error Response:**

    {
        "status": false,
        "message": "Error message"
    }

### 5\. Find Specific IHA (/api/iha/find)

Retrieves specific IHA details based on query parameters such as brand, model, weight, category, and price.

    GET /api/iha/find?brand=[brand]&model=[model]&weight=[weight]&category=[category]&price=[price]
    Header:
        Authorization: [your_token_here]

**Query Parameters:**

- `brand` (optional): Filter IHAs by brand.
- `model` (optional): Filter IHAs by model.
- `weight` (optional): Filter IHAs by weight.
- `category` (optional): Filter IHAs by category.
- `price` (optional): Filter IHAs by price.

**Response:**

    {
        "status": true,
        "message": "IHA information retrieved successfully.",
        "data": [
            {
                "brand": "Brand Name",
                "model": "Model",
                "weight": "Weight",
                "category": "Category",
                "price": "Price"
            },
            ...
        ]
    }

**Error Response:**

    {
        "status": false,
        "message": "Error message"
    }

# API Usage for Customer

## API Endpoints and Usage

### 1\. List Customers (/api/customers)

    GET /api/customers
    Header:
        Authorization: [your_token_here]

**Error Response:**

    {
        "status": false,
        "message": "Error message"
    }

### 2\. Create Customer (/api/customer/create)

    POST /api/customer/create
    Header:
        Authorization: [your_token_here]
    Body:
        {
            "firstName": "First Name",
            "lastName": "Last Name",
            "email": "email@example.com",
            "phoneNumber": "1234567890"
        }

**Error Response:**

    {
        "status": false,
        "message": "Error message"
    }

### 3\. Delete Customer (/api/customer/delete/<customer_id>)

    DELETE /api/customer/delete/[customer_id]
    Header:
        Authorization: [your_token_here]

### 4\. Update Customer (/api/customer/update/<customer_id>)

    PUT /api/customer/update/[customer_id]
    Header:
        Authorization: [your_token_here]
    Body:
        {
            "firstName": "New First Name",
            "lastName": "New Last Name",
            "email": "newemail@example.com",
            "phoneNumber": "0987654321"
        }

**Error Response:**

    {
        "status": false,
        "message": "Error message"
    }

### 5\. Find Specific Customer (/api/customer/find)

This endpoint allows for retrieving specific customer details based on various query parameters such as ID, name, surname, and username.

    GET /api/customer/find?id=[id]&name=[name]&surname=[surname]&username=[username]
    Header:
        Authorization: [your_token_here]

**Query Parameters:**

- `id` (optional): Filter customers by their unique ID.
- `name` (optional): Filter customers by their first name.
- `surname` (optional): Filter customers by their surname.
- `username` (optional): Filter customers by their username.

**Successful Response:**

    {
        "status": true,
        "message": "Customers retrieved successfully.",
        "data": [
            {
                "id": "Customer ID",
                "name": "First Name",
                "surname": "Surname",
                "username": "Username"
            },
            ...
        ]
    }

**Error Response:**

    {
        "status": false,
        "message": "Error message"
    }

Detailed API Usage for Reservation App body { font-family: Arial, sans-serif; margin: 20px; } h1 { color: #333; } h2, h3 { color: #555; } p, pre { margin-left: 20px; } pre { background-color: #f4f4f4; padding: 10px; }

# Detailed API Usage for Reservation App

This document provides detailed examples on how to use each API endpoint in the Reservation App, including the required Authorization header and request body for POST requests.

/v1/ is reserved exclusively for admin access, while /api/ is designated solely for customer use.

# API Usage for IHA

## API Endpoints and Usage

### 1\. List IHAs (/api/ihas)

Retrieves a list of all IHAs.

    GET /api/ihas
    Header:
        Authorization: [your_token_here]

**Error Response:**

    {
        "status": false,
        "message": "Error message"
    }

### 2\. Create IHA (/v1/iha/create)

Creates a new IHA. Requires details about the IHA in the request body.

    POST /v1/iha/create
    Header:
        Content-Type: application/json
        Authorization: [your_token_here]
    Body:
        {
            "brand": "IHA Brand",
            "model": "Model",
            "weight": "Weight",
            "category": "Category",
            "price": "Price",
            "image": "Optional image file"
        }

**Successful Response:**

    {
        "status": true,
        "message": "IHA creation successful.",
        "data": {
            "id": "IHA ID",
            "brand": "IHA Brand",
            "model": "Model",
            "weight": "Weight",
            "category": "Category",
            "price": "Price",
            "image_url": "Optional image URL"
        }
    }

**Error Response:**

    {
        "status": false,
        "message": "Error message"
    }

### 3\. Delete IHA (/v1/iha/delete/<iha_id>)

Deletes a specific IHA by ID. Replace <iha_id> with the actual ID of the IHA you want to delete.

    DELETE /v1/iha/delete/[iha_id]
    Header:
        Authorization: [your_token_here]

**Error Response:**

    {
        "status": false,
        "message": "Error message"
    }

### 4\. Update IHA (/v1/iha/update/<iha_id>)

Updates the details of a specific IHA. Provide the new details in the request body.

    PUT /v1/iha/update/[iha_id]
    Header:
        Authorization: [your_token_here]
    Body:
        {
            "name": "New Name",
            "model": "New Model",
            ...
        }

**Error Response:**

    {
        "status": false,
        "message": "Error message"
    }

### 5\. Find Specific IHA (/api/iha/find)

Retrieves specific IHA details based on query parameters such as brand, model, weight, category, and price.

    GET /api/iha/find?brand=[brand]&model=[model]&weight=[weight]&category=[category]&price=[price]
    Header:
        Authorization: [your_token_here]

**Query Parameters:**

- `brand` (optional): Filter IHAs by brand.
- `model` (optional): Filter IHAs by model.
- `weight` (optional): Filter IHAs by weight.
- `category` (optional): Filter IHAs by category.
- `price` (optional): Filter IHAs by price.

**Response:**

    {
        "status": true,
        "message": "IHA information retrieved successfully.",
        "data": [
            {
                "brand": "Brand Name",
                "model": "Model",
                "weight": "Weight",
                "category": "Category",
                "price": "Price"
            },
            ...
        ]
    }

**Error Response:**

    {
        "status": false,
        "message": "Error message"
    }

# API Usage for Customer

## API Endpoints and Usage

### 1\. List Customers (/api/customers)

    GET /api/customers
    Header:
        Authorization: [your_token_here]

**Error Response:**

    {
        "status": false,
        "message": "Error message"
    }

### 2\. Create Customer (/api/customer/create)

    POST /api/customer/create
    Header:
        Authorization: [your_token_here]
    Body:
        {
            "firstName": "First Name",
            "lastName": "Last Name",
            "email": "email@example.com",
            "phoneNumber": "1234567890"
        }

**Error Response:**

    {
        "status": false,
        "message": "Error message"
    }

### 3\. Delete Customer (/api/customer/delete/<customer_id>)

    DELETE /api/customer/delete/[customer_id]
    Header:
        Authorization: [your_token_here]

### 4\. Update Customer (/api/customer/update/<customer_id>)

    PUT /api/customer/update/[customer_id]
    Header:
        Authorization: [your_token_here]
    Body:
        {
            "firstName": "New First Name",
            "lastName": "New Last Name",
            "email": "newemail@example.com",
            "phoneNumber": "0987654321"
        }

**Error Response:**

    {
        "status": false,
        "message": "Error message"
    }

### 5\. Find Specific Customer (/api/customer/find)

This endpoint allows for retrieving specific customer details based on various query parameters such as ID, name, surname, and username.

    GET /api/customer/find?id=[id]&name=[name]&surname=[surname]&username=[username]
    Header:
        Authorization: [your_token_here]

**Query Parameters:**

- `id` (optional): Filter customers by their unique ID.
- `name` (optional): Filter customers by their first name.
- `surname` (optional): Filter customers by their surname.
- `username` (optional): Filter customers by their username.

**Successful Response:**

    {
        "status": true,
        "message": "Customers retrieved successfully.",
        "data": [
            {
                "id": "Customer ID",
                "name": "First Name",
                "surname": "Surname",
                "username": "Username"
            },
            ...
        ]
    }

**Error Response:**

    {
        "status": false,
        "message": "Error message"
    }

Detailed API Usage for Reservation App body { font-family: Arial, sans-serif; margin: 20px; } h1 { color: #333; } h2, h3 { color: #555; } p, pre { margin-left: 20px; } pre { background-color: #f4f4f4; padding: 10px; }

# Detailed API Usage for Reservation App

This document provides detailed examples on how to use each API endpoint in the Reservation App, including the required Authorization header and request body for POST requests.

/v1/ is reserved exclusively for admin access, while /api/ is designated solely for customer use.

# API Usage for IHA

## API Endpoints and Usage

### 1\. List IHAs (/api/ihas)

Retrieves a list of all IHAs.

    GET /api/ihas
    Header:
        Authorization: [your_token_here]

**Error Response:**

    {
        "status": false,
        "message": "Error message"
    }

### 2\. Create IHA (/v1/iha/create)

Creates a new IHA. Requires details about the IHA in the request body.

    POST /v1/iha/create
    Header:
        Content-Type: application/json
        Authorization: [your_token_here]
    Body:
        {
            "brand": "IHA Brand",
            "model": "Model",
            "weight": "Weight",
            "category": "Category",
            "price": "Price",
            "image": "Optional image file"
        }

**Successful Response:**

    {
        "status": true,
        "message": "IHA creation successful.",
        "data": {
            "id": "IHA ID",
            "brand": "IHA Brand",
            "model": "Model",
            "weight": "Weight",
            "category": "Category",
            "price": "Price",
            "image_url": "Optional image URL"
        }
    }

**Error Response:**

    {
        "status": false,
        "message": "Error message"
    }

### 3\. Delete IHA (/v1/iha/delete/<iha_id>)

Deletes a specific IHA by ID. Replace <iha_id> with the actual ID of the IHA you want to delete.

    DELETE /v1/iha/delete/[iha_id]
    Header:
        Authorization: [your_token_here]

**Error Response:**

    {
        "status": false,
        "message": "Error message"
    }

### 4\. Update IHA (/v1/iha/update/<iha_id>)

Updates the details of a specific IHA. Provide the new details in the request body.

    PUT /v1/iha/update/[iha_id]
    Header:
        Authorization: [your_token_here]
    Body:
        {
            "name": "New Name",
            "model": "New Model",
            ...
        }

**Error Response:**

    {
        "status": false,
        "message": "Error message"
    }

### 5\. Find Specific IHA (/api/iha/find)

Retrieves specific IHA details based on query parameters such as brand, model, weight, category, and price.

    GET /api/iha/find?brand=[brand]&model=[model]&weight=[weight]&category=[category]&price=[price]
    Header:
        Authorization: [your_token_here]

**Query Parameters:**

- `brand` (optional): Filter IHAs by brand.
- `model` (optional): Filter IHAs by model.
- `weight` (optional): Filter IHAs by weight.
- `category` (optional): Filter IHAs by category.
- `price` (optional): Filter IHAs by price.

**Response:**

    {
        "status": true,
        "message": "IHA information retrieved successfully.",
        "data": [
            {
                "brand": "Brand Name",
                "model": "Model",
                "weight": "Weight",
                "category": "Category",
                "price": "Price"
            },
            ...
        ]
    }

**Error Response:**

    {
        "status": false,
        "message": "Error message"
    }

# API Usage for Customer

## API Endpoints and Usage

### 1\. List Customers (/api/customers)

    GET /api/customers
    Header:
        Authorization: [your_token_here]

**Error Response:**

    {
        "status": false,
        "message": "Error message"
    }

### 2\. Create Customer (/api/customer/create)

    POST /api/customer/create
    Header:
        Authorization: [your_token_here]
    Body:
        {
            "firstName": "First Name",
            "lastName": "Last Name",
            "email": "email@example.com",
            "phoneNumber": "1234567890"
        }

**Error Response:**

    {
        "status": false,
        "message": "Error message"
    }

### 3\. Delete Customer (/api/customer/delete/<customer_id>)

    DELETE /api/customer/delete/[customer_id]
    Header:
        Authorization: [your_token_here]

### 4\. Update Customer (/api/customer/update/<customer_id>)

    PUT /api/customer/update/[customer_id]
    Header:
        Authorization: [your_token_here]
    Body:
        {
            "firstName": "New First Name",
            "lastName": "New Last Name",
            "email": "newemail@example.com",
            "phoneNumber": "0987654321"
        }

**Error Response:**

    {
        "status": false,
        "message": "Error message"
    }

### 5\. Find Specific Customer (/api/customer/find)

This endpoint allows for retrieving specific customer details based on various query parameters such as ID, name, surname, and username.

    GET /api/customer/find?id=[id]&name=[name]&surname=[surname]&username=[username]
    Header:
        Authorization: [your_token_here]

**Query Parameters:**

- `id` (optional): Filter customers by their unique ID.
- `name` (optional): Filter customers by their first name.
- `surname` (optional): Filter customers by their surname.
- `username` (optional): Filter customers by their username.

**Successful Response:**

    {
        "status": true,
        "message": "Customers retrieved successfully.",
        "data": [
            {
                "id": "Customer ID",
                "name": "First Name",
                "surname": "Surname",
                "username": "Username"
            },
            ...
        ]
    }

**Error Response:**

    {
        "status": false,
        "message": "Error message"
    }

# API Usage for Reservation

## API Endpoints and Usage

### 1\. List Reservations (/api/reservations)

    GET /api/reservations
    Header:
        Authorization: [your_token_here]

**Error Response:**

    {
        "status": false,
        "message": "Error message"
    }

### 2\. Create Reservation (/api/reservation/create)

    POST /api/reservation/create
    Header:
        Authorization: [your_token_here]
    Body:
        {
            "customerId": "Customer ID",
            "ihaId": "IHA ID",
            "reservationDate": "YYYY-MM-DD",
            "durationHours": "Number of Hours"
        }

**Error Response:**

    {
        "status": false,
        "message": "Error message"
    }

### 3\. Delete Reservation (/api/reservation/delete/<reservation_id>)

    DELETE /api/reservation/delete/[reservation_id]
    Header:
        Authorization: [your_token_here]

**Error Response:**

    {
        "status": false,
        "message": "Error message"
    }

### 4\. Update Reservation (/api/reservation/update/<reservation_id>)

    PUT /api/reservation/update/[reservation_id]
    Header:
        Authorization: [your_token_here]
    Body:
        {
            "customerId": "New Customer ID",
            "ihaId": "New IHA ID",
            "reservationDate": "NewNew YYYY-MM-DD",
            "durationHours": "New Number of Hours"
        }

**Error Response:**

    {
        "status": false,
        "message": "Error message"
    }

### 5\. Find Specific Reservation (/api/reservation/find)

This endpoint allows for retrieving specific reservation details based on various query parameters such as reservation ID, start date range, IHA brand/model, and customer details.

    GET /api/reservation/find?reservation_id=[reservation_id]&start_date_from=[start_date_from]&start_date_to=[start_date_to]&iha_brand=[iha_brand]&iha_model=[iha_model]&customer_name=[customer_name]&customer_surname=[customer_surname]&customer_username=[customer_username]
    Header:
        Authorization: [your_token_here]

**Query Parameters:**

- `reservation_id` (optional): Filter reservations by their unique ID.
- `start_date_from` (optional): Filter reservations starting from this date.
- `start_date_to` (optional): Filter reservations ending to this date.
- `iha_brand` (optional): Filter reservations by IHA brand.
- `iha_model` (optional): Filter reservations by IHA model.
- `customer_name` (optional): Filter reservations by customer's first name.
- `customer_surname` (optional): Filter reservations by customer's surname.
- `customer_username` (optional): Filter reservations by customer's username.

**Successful Response:**

    {
        "status": true,
        "message": "Reservations retrieved successfully.",
        "data": [
            {
                "reservation_id": "Reservation ID",
                "iha": {
                    "brand": "Brand",
                    "model": "Model",
                    "category": "Category",
                    "price": "Price"
                },
                "customer": {
                    "name": "Name",
                    "surname": "Surname",
                    "username": "Username"
                },
                "start_date": "Start Date",
                "finish_date": "Finish Date",
                "total_price": "Total Price"
            },
            ...
        ]
    }

**Error Response:**

    {
        "status": false,
        "message": "Error message"
    }
