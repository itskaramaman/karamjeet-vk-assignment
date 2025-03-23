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
python main.py # Run the Flask backend
# The Flask backend will be available at: http://127.0.0.1:5000


# After that, run the frontend:
cd frontend
npm run dev # Start the React app
# The React frontend will be available at: http://localhost:5173
```

### Bonus: Frontend UI with Category Filtering

The React frontend provides a simple and user-friendly interface to display the scraped news articles. Key features include:

- **Category Filtering**: Users can filter the news data by specific categories (e.g., "Sports", "Technology", "Business") and subcategories (e.g., "Football", "Cricket").
- **Pagination**: The frontend supports pagination to display large sets of news data in manageable chunks.

- **UI Components**:
  - A dropdown to select categories.
  - A dropdown to select subcategories (depending on the selected category).
  - A list of articles that updates dynamically based on the user's filtering choices.

#### How to Use the Frontend:

Once the frontend is running (`npm run dev`), navigate to the browser window where it’s hosted (usually at `http://localhost:3000`).

- **Select a Category**: The first dropdown lets you choose a general category (e.g., Sports, Technology, Business).
- **Select a Subcategory**: If applicable, select a subcategory to further filter articles (e.g., "Football" under "Sports").
- **Articles List**: After selecting a category and/or subcategory, the news articles matching your criteria will be displayed.
- **Pagination**: If there are many results, pagination will break the articles into pages for easier navigation.

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

## AI Usage

During the development of this project, AI tools (like OpenAI's ChatGPT) were used in the following areas:

- **Web Scraping**: I used AI to help identify the best class names and CSS selectors for scraping news data from the BBC website. Some prompts used include:
  - "Can you help me find the correct CSS selectors for the BBC News I will provide a news card?"
  - "What are the best strategies for web scraping dynamic content with Selenium?"
- **ChromeDriver Debugging**: AI was used to troubleshoot issues with ChromeDriver not working correctly. Sample prompts used include:
  - "How do I resolve issues with ChromeDriver not launching in headless mode?"
  - "Which version will work for Chrome should i update it to the latest?"
- **Documentation**: AI tools were used to refine the README.md and ensure all details, such as installation, usage, and features, were clear. Some example prompts include:
  - "Can you generate a detailed README.md for a web scraping project?"
  - "How should I document the installation process for a Flask app?"
- **Debugging News Fetching**: During development, I used AI to resolve issues where some sports news could not be fetched. Prompts included:
  - "What might cause certain elements not to be scraped on the BBC innovation page?"

AI tools were used as a valuable aid to ensure the project was developed efficiently and accurately, while all design choices and development steps were thoroughly documented.

AI tools were used as an aid to enhance development efficiency and improve the overall quality of the project.

## Technical Requirements

This project was developed from scratch and does not use any pre-existing repositories or ready-made code for scraping the BBC website. The scraping logic was designed specifically for this project, adhering to the guidelines provided.
