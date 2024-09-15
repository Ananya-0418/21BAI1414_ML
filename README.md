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
