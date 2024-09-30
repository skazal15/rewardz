# Student Book Rental Web Application

A Django web application for managing student book rental with integration to the OpenLibrary API.

## Features

- **Free Rental Period:** Rent books free for one month.
- **Automatic Fee Calculation:** Fees apply after the free month based on page count divided by 100.
- **Admin Interface:**
  - Start new rental.
  - Extend existing rental.
  - View student rental dashboards with fee details.

## Table of Contents

- [Installation](#installation)
- [Usage](#usage)
- [Running Tests](#running-tests)
- [Notes](#notes)
- [License](#license)

## Installation

### Prerequisites

- Python 3.8+
- Git
- Virtualenv (optional but recommended)

### Steps

1. **Clone the Repository**

   ```bash
   git clone https://github.com/yourusername/bookrental.git
   cd bookrental

2. **Create and Activate Virtual Environment**

   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install Dependencies**

   ```bash
   pip install -r requirements.txt

4. **Apply Migrations**

   ```bash
   python manage.py makemigrations
   python manage.py migrate
   ```

5. **Create Superuser**

   ```bash
   python manage.py createsuperuser
   ```

6. **Run Development Server**

   ```bash
   python manage.py runserver
   ```

7. **Access the Application**

   ```bash
   Admin Site: http://localhost:8000/admin/
   Start Rental: http://localhost:8000/rental/start/
   Extend Rental: http://localhost:8000/rental/extend/
   ```

## Usage

### Admin Actions:

- Log in to the admin site using your superuser credentials.
- Add students (users) who will rent books.

### Start Rental:

- Navigate to /rental/start/.
- Fill in the student's name and the book title.
- The system fetches book details from the OpenLibrary API.

### Extend an Existing Rental:

- Navigate to /rental/extend/.
- Select the rental to extend.
- Fees are automatically calculated based on the overdue period.

### View Student Dashboard:

- Navigate to /rental/dashboard/<user_id>/.
- Replace <user_id> with the student's ID.

## Running Tests

   ```bash
    python manage.py test rental
   ```

## Notes

- **Internet Connection:** Required to fetch data from the OpenLibrary API.
- **Fee Calculation:** Fees are updated each time rental details or the dashboard are viewed.
- **Customization:** The application can be extended with additional features like user authentication for students.

