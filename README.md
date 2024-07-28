# Daily Expenses Sharing Application

This is a Django REST framework-based application to manage and share daily expenses among users. The application allows users to register, login, add expenses, and split them based on three different methods: exact amounts, percentages, and equal splits. Additionally, users can download balance sheets summarizing their financial interactions.

## Features

- User registration and authentication using JWT
- Adding and managing expenses
- Splitting expenses equally, by exact amounts, or by percentages
- Viewing individual and overall expenses
- Downloading balance sheets

## Requirements

- Python 3.8+
- Django 3.2+
- Django REST Framework 3.12+
- djangorestframework-simplejwt 4.7.2+

## Setup Instructions

### Step 1: Clone the Repository

```bash
git clone https://github.com/yourusername/expenses-sharing-backend.git
cd expenses_sharing_project
```

### Step 2: Create and Activate a Virtual Environment

```bash
python -m venv venv
venv/Scripts/activate   # On Linux use `source venv/bin/activate`
```

### Step 3: Install Dependencies

```bash
pip install -r requirements.txt
```

### Step 4: Apply Migrations

```bash
python manage.py migrate
```

### Step 5: Run the Development Server

```bash
python manage.py runserver
```

## API Endpoints

### User Registration

**Endpoint**: `POST /api/register/`

**Request Body**:

```json
{
  "email": "user@example.com",
  "name": "User Name",
  "mobile": "1234567890",
  "password": "password123"
}
```

**Response**:

```json
{
  "id": 1,
  "email": "user@example.com",
  "name": "User Name",
  "mobile": "1234567890"
}
```

### User Login

**Endpoint**: `POST /api/login/`

**Request Body**:

```json
{
  "email": "user@example.com",
  "password": "password123"
}
```

**Response**:

```json
{
  "access": "your_access_token",
  "refresh": "your_refresh_token"
}
```

### Add Expense

**Endpoint**: `POST /api/expenses/`

**Request Headers**:

```
Authorization: Bearer your_access_token
```

**Request Body**:

```json
{
    "title": "Dinner",
    "amount": 3000.00,
    "split_method": "equal", or "exact" or "percentage"
    "created_by": 1,
    "participants": [
        {"user": 1},
        {"user": 2},
        {"user": 3}
    ]
}
```

**Response**:

```json
{
  "id": 1,
  "title": "Dinner",
  "amount": 3000.0,
  "split_method": "equal",
  "created_by": 1,
  "participants": [
    { "user": 1, "amount": 1000.0 },
    { "user": 2, "amount": 1000.0 },
    { "user": 3, "amount": 1000.0 }
  ]
}
```

### Retrieve Individual User Expenses

**Endpoint**: `GET /api/expenses/user/`

**Request Headers**:

```
Authorization: Bearer your_access_token
```

**Response**:

```json
[
  {
    "id": 1,
    "title": "Dinner",
    "amount": 3000.0,
    "split_method": "equal",
    "created_by": 1,
    "participants": [
      { "user": 1, "amount": 1000.0 },
      { "user": 2, "amount": 1000.0 },
      { "user": 3, "amount": 1000.0 }
    ]
  }
]
```

### Retrieve Overall Expenses

**Endpoint**: `GET /api/expenses/all/`

**Request Headers**:

```
Authorization: Bearer your_access_token
```

**Response**:

```json
[
  {
    "id": 1,
    "title": "Dinner",
    "amount": 3000.0,
    "split_method": "equal",
    "created_by": 1,
    "participants": [
      { "user": 1, "amount": 1000.0 },
      { "user": 2, "amount": 1000.0 },
      { "user": 3, "amount": 1000.0 }
    ]
  }
]
```

### Download Balance Sheet

**Endpoint**: `GET /api/expenses/balance_sheet/`

**Request Headers**:

```
Authorization: Bearer your_access_token
```

**Response**:
This will prompt the download of a CSV file. The content of the CSV file might look like this:

```
User,Total Amount Owed
user1@example.com,2500.00
user2@example.com,1500.00
user3@example.com,1500.00
```

### Retrieve User Details

**Endpoint**: `GET /api/user/`

**Request Headers**:

```
Authorization: Bearer your_access_token
```

**Response**:

```json
{
  "id": 1,
  "email": "user1@example.com",
  "name": "User One",
  "mobile": "1234567890"
}
```

## License

This project is licensed under the MIT License.
