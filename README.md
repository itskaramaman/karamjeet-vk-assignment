# BBC Web Scrapper

This project provides a Flask-based REST API that allows you to scrape and store news data from BBC News and BBC Sport, with functionality for retrieving stored news and sports articles with pagination. The API interacts with a SQLite database to store the scraped news items.

## Features

- Scrape news data from various categories (e.g., General, Technology, Business, Sports) using web scraping techniques with Selenium.
- Store the scraped data in a SQLite database.
- Retrieve scraped news data, including pagination and filtering by category and subcategory (e.g., "Football" or "Cricket").
- Delete news items from the database by ID.

## Technology Stack

- **Backend**: Flask (Python Web Framework)
- **Database**: SQLite (SQLAlchemy ORM for database interaction)
- **Web Scraping**: Selenium WebDriver with Python
- **Cross-Origin Resource Sharing (CORS)**: Flask-CORS
- **WebDriver**: ChromeDriver (Headless mode)
- **Frontend**: React.js

## Prerequisites

Before running this project, make sure you have the following installed:

- Python 3.6 or higher
- `pip` (Python package installer)

## Installation

Follow these steps to set up the project on your local machine.

### 1. Clone the repository

Start by cloning the repository to your local machine:

```bash
git clone https://github.com/itskaramaman/karamjeet-vk-assignment.git
cd karamjeet-vk-assignment
```

### 2. Set up a virtual environment (Optional but recommended)

To isolate your project dependencies, it’s recommended to create a virtual environment:

For Linux/Mac:

```bash
python3 -m venv venv
source venv/bin/activate
```

For Windows:

```bash
python -m venv venv
.\venv\Scripts\activate
```

### 3. Install dependencies

Once your virtual environment is activated, install the required packages by running:

```bash
cd backend
pip install -r requirements.txt

cd frontend
npm install --legacy-peer-deps
```

### 4. Running the backend and frontend

```bash
cd backend
python manage.py

cd frontend
npm run dev
```

## API Endpoints

### 1. `GET /scrape-news`
- **Description**: Triggers the scraping of BBC News articles and stores the data in the SQLite database.

### 2. `GET /data`
- **Description**: Retrieves all the news data (with pagination). Supports filtering by category and subcategory.

### 3. `GET /data/<category>`
- **Description**: Retrieves news data filtered by a specific category (e.g., "Sports", "Technology").

### 4. `GET /data/<category>/<sub_category>`
- **Description**: Retrieves news data filtered by a specific category and subcategory (e.g., "Sports/Football").

### 5. `DELETE /delete/<id>`
- **Description**: Deletes a specific news item from the database using its unique ID.
