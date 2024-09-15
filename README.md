A Flask-based web application that provides trademark document search functionality, with caching using Redis and MongoDB for storing user data and documents. The application also features rate limiting to control excessive API usage and a background scraper to keep the database updated.


Table of Contents
Features
Technology Stack
Installation
Configuration
Usage
API Endpoints
Contributing
License

Features
Document Search: Allows users to search for documents based on text input.
Caching with Redis: Speeds up search results by caching frequent queries.
Rate Limiting: Controls the number of API requests users can make in a specified time frame.
MongoDB Integration: Stores user logs and document data.
Background Scraping: Automatically updates the database with new documents every hour.
Error Handling: Provides informative error messages and logs.

Technology Stack
Backend Framework: Flask
Database: MongoDB
Caching and Rate Limiting: Redis
Background Scraper: Python with threading
APIs: RESTful API

Installation
Clone the repository:
git clone https://github.com/your-username/Trade_mark1414.git
Set up a virtual environment:
python -m venv venv

Install the required dependencies:
pip install -r requirements.txt

Set up MongoDB:

Create a MongoDB cluster and update the MongoDB connection string in app.py.
Set up Redis:

Install Redis on your system and make sure it is running.
Update the Redis configuration in redis_setup.py.

Configuration
Before running the application, ensure that the following configurations are correctly set in the project files:

MongoDB: Update your MongoDB connection string in the app.py file:
client = MongoClient('mongodb+srv://ananyasundar2004:123@cluster0.tf1ob.mongodb.net/')
Redis: Make sure Redis is running locally or update the connection details in redis_setup.py:
redis_client = RedisClient(host='localhost', port=6379, decode_responses=True).client

Usage
Run the Flask application:

bash
flask run
The application will start running locally at http://127.0.0.1:5000/.

You can interact with the API using tools like Postman or cURL.

API Endpoints
1. Health Check
Endpoint: /health
Method: GET
Description: Checks if the API is active.
Response
{
  "status": "API is active"
}

Search Documents
Endpoint: /search
Method: POST
Request Body:
{
  "user_id": "123",
  "text": "Trademark name",
  "top_k": 5,
  "threshold": 0.5
}
Response:
{
  "inference_time": "25.20ms",
  "source": "db",
  "results": [
    {
      "_id": "document_id",
      "title": "Document title",
      ...
    }
  ]
}


Rate Limiting
The application returns a 429 Too Many Requests error when the rate limit is exceeded
{
  "error": "Too many requests"
}

Contributing
Contributions are welcome! To contribute:

Fork the repository.
Create a new branch for your feature/bug fix.
Make the necessary changes and commit.
Push the branch to your forked repository.
Open a pull request to the main repository.

License
This project is licensed under the MIT License. See the LICENSE file for details.

Contact
For any queries or issues, feel free to contact the project maintainer at ananyasundar.2004@gmail.com.
