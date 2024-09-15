# **Trademark Search Application**

### A Flask-based web application that provides trademark document search functionality, with caching using Redis and MongoDB for storing user data and documents. The application also features rate limiting to control excessive API usage and a background scraper to keep the database updated.

---

## **Table of Contents**
1. [Features](#features)
2. [Technology Stack](#technology-stack)
3. [Installation](#installation)
4. [Configuration](#configuration)
5. [Usage](#usage)
6. [API Endpoints](#api-endpoints)
7. [Contributing](#contributing)
8. [License](#license)

---

## **Features**

- **Document Search**: Allows users to search for documents based on text input.
- **Caching with Redis**: Speeds up search results by caching frequent queries.
- **Rate Limiting**: Controls the number of API requests users can make in a specified time frame.
- **MongoDB Integration**: Stores user logs and document data.
- **Background Scraping**: Automatically updates the database with new documents every hour.
- **Error Handling**: Provides informative error messages and logs.

---

## **Technology Stack**

- **Backend Framework**: Flask
- **Database**: MongoDB
- **Caching and Rate Limiting**: Redis
- **Background Scraper**: Python with threading
- **APIs**: RESTful API

---

## **Installation**

1. Clone the repository:
   ```bash
   git clone https://github.com/your-username/Trade_mark1414.git 
   ```

2. Navigate to the project directory:
  ```bash
   cd Trade_mark1414 
   ```

3. Create and activate a virtual environment:
  ```bash
   python -m venv venv
```
4. Install the required dependencies:
   ```bash
   pip install -r requirements.txt
   ```
5. Set up environment variables:
   ```bash
   MONGO_URI=your_mongodb_uri
   REDIS_HOST=localhost
   REDIS_PORT=6379
   ```
6. Run the application:
   ```bash
   python app.py

## **configurations**

- **MongoDB**: Ensure that your MongoDB URI is properly set up in the .env file.
- **Redis:**: Ensure that Redis is running locally on localhost:6379 or update the .env file with your Redis host and port.



