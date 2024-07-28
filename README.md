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
python manage.py makemigrations
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
  "amount": 3000.0,
  "split_method": "equal",
  "created_by": 1,
  "participants": [{ "user": 1 }, { "user": 2 }, { "user": 3 }]
}
```

**Response**:

```json
{
  "id": 1,
  "title": "Cricket",
  "amount": 5000.0,
  "split_method": "equal",
  "created_by": 1,
  "created_by_name": "User One",
  "participants": [
    {
      "user": "123123",
      "user_name": "User One",
      "amount": "1666.67",
      "percentage": null
    },
    {
      "user": "111222",
      "user_name": "User Two",
      "amount": "1666.67",
      "percentage": null
    },
    {
      "user": "444555",
      "user_name": "User Three",
      "amount": "1666.67",
      "percentage": null
    }
  ]
}
```

**percentage method:**

```json
{
  "title": "Football",
  "amount": 7000.0,
  "split_method": "percentage",
  "created_by": 1,
  "participants": [
    { "user": "2", "percentage": 50.0 },
    { "user": "3", "percentage": 25.0 },
    { "user": "4", "percentage": 25.0 }
  ]
}
```

**Response:**

```json
{
  "id": 2,
  "title": "Football",
  "amount": "7000.00",
  "split_method": "percentage",
  "created_by": 1,
  "created_by_name": "User One",
  "participants": [
    {
      "user": "2",
      "user_name": "User One",
      "amount": "3500.00",
      "percentage": "50.00"
    },
    {
      "user": "3",
      "user_name": "User Two",
      "amount": "1750.00",
      "percentage": "25.00"
    },
    {
      "user": "4",
      "user_name": "User Three",
      "amount": "1750.00",
      "percentage": "25.00"
    }
  ]
}
```

**Exact method:**

```json
{
  "title": "Shopping",
  "amount": 4299.0,
  "split_method": "exact",
  "created_by": 1,
  "participants": [
    { "user": 1, "amount": 799.0 },
    { "user": 2, "amount": 2000.0 },
    { "user": 3, "amount": 1500.0 }
  ]
}
```

**Response:**

```json
{
  "id": 5,
  "title": "Shopping",
  "amount": "4299.00",
  "split_method": "exact",
  "created_by": 8,
  "created_by_name": "John star",
  "participants": [
    {
      "user": 1,
      "user_name": "John Doe",
      "amount": "799.00",
      "percentage": null
    },
    {
      "user": 7,
      "user_name": "John edus",
      "amount": "2000.00",
      "percentage": null
    },
    {
      "user": 6,
      "user_name": "John dus",
      "amount": "1500.00",
      "percentage": null
    }
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
    "id": 5,
    "title": "Shopping",
    "amount": 4299.0,
    "split_method": "exact",
    "created_by": 8,
    "participants": [
      {
        "user": 1,
        "amount": 799.0
      },
      {
        "user": 7,
        "amount": 2000.0
      },
      {
        "user": 6,
        "amount": 1500.0
      }
    ]
  }
]
```

The response indicates that the user with ID 7 is listed as a participant in the expense

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
      {
        "user": 1,
        "amount": 1000.0
      },
      {
        "user": 2,
        "amount": 1000.0
      },
      {
        "user": 3,
        "amount": 1000.0
      }
    ]
  },
  {
    "id": 2,
    "title": "Dinner",
    "amount": 3000.0,
    "split_method": "equal",
    "created_by": 7,
    "participants": [
      {
        "user": 1,
        "amount": 1000.0
      },
      {
        "user": 2,
        "amount": 1000.0
      },
      {
        "user": 3,
        "amount": 1000.0
      }
    ]
  },
  {
    "id": 3,
    "title": "Cricket",
    "amount": 5000.0,
    "split_method": "equal",
    "created_by": 8,
    "participants": [
      {
        "user": 1,
        "amount": 1666.67
      },
      {
        "user": 2,
        "amount": 1666.67
      },
      {
        "user": 3,
        "amount": 1666.67
      }
    ]
  },
  {
    "id": 4,
    "title": "Football",
    "amount": 7000.0,
    "split_method": "percentage",
    "created_by": 8,
    "participants": [
      {
        "user": 3,
        "amount": 3500.0
      },
      {
        "user": 4,
        "amount": 1750.0
      },
      {
        "user": 6,
        "amount": 1750.0
      }
    ]
  },
  {
    "id": 5,
    "title": "Shopping",
    "amount": 4299.0,
    "split_method": "exact",
    "created_by": 8,
    "participants": [
      {
        "user": 1,
        "amount": 799.0
      },
      {
        "user": 7,
        "amount": 2000.0
      },
      {
        "user": 6,
        "amount": 1500.0
      }
    ]
  }
]
```

The response from the `/api/expenses/all/` endpoint provides a list of all expenses in the system. Each expense entry includes details about the expense itself, the creator, and the participants with their respective shares. Here's a breakdown of the response:

```json
{
  "id": 1,
  "title": "Dinner",
  "amount": 3000.0,
  "split_method": "equal",
  "created_by": 1,
  "participants": [
    {
      "user": 1,
      "amount": 1000.0
    },
    {
      "user": 2,
      "amount": 1000.0
    },
    {
      "user": 3,
      "amount": 1000.0
    }
  ]
}
```

**Title: Dinner
Amount: 3000.00
Split Method: Equal
Created By: User with ID 1
Participants:
User 1: 1000.00
User 2: 1000.00
User 3: 1000.00**

### Download Balance Sheet

**Endpoint**: `GET /api/expenses/balance_sheet/`

**Request Headers**:

```
Authorization: Bearer your_access_token
```

**Response**:
This will prompt the download of a CSV file. The content of the CSV file might look like this:
**Breakdown:**
CSV file provides two sections: individual expenses for the authenticated user and overall expenses for all users.

**This section lists the expenses where user7@example.com is a participant:**

```
Expense,User,Amount
Shopping,user7@example.com,2000.00
```

**This section lists all expenses in the system, showing each participant's share:**

```
Overall Expenses
Expense,User,Amount
Dinner,user@example.com,1000.00
Dinner,user2@example.com,1000.00
Dinner,user3@example.com,1000.00
Dinner,user@example.com,1000.00
Dinner,user2@example.com,1000.00
Dinner,user3@example.com,1000.00
Cricket,user@example.com,1666.67
Cricket,user2@example.com,1666.67
Cricket,user3@example.com,1666.67
Football,user3@example.com,3500.00
Football,user4@example.com,1750.00
Football,user6@example.com,1750.00
Shopping,user@example.com,799.00
Shopping,user7@example.com,2000.00
Shopping,user6@example.com,1500.00
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
