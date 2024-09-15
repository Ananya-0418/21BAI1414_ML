# from flask import Flask, request, jsonify
# from pymongo import MongoClient
# from redis import Redis
# from bs4 import BeautifulSoup
# import requests
# import threading
# import time
# import json

# app = Flask(__name__)

# # MongoDB setup
# client = MongoClient('mongodb+srv://ananyasundar2004:123@cluster0.tf1ob.mongodb.net/')
# db = client['Trade_1414']
# users_collection = db['users']
# documents_collection = db['Documents']

# # Redis setup
# redis_client = Redis(host='localhost', port=6379, decode_responses=True)

# # Helper function for caching
# def cache_response(query, result):
#     redis_client.set(query, json.dumps(result), ex=60)  # Cache for 1 hour

# # Rate limiting function
# def rate_limit(user_id):
#     key = f"user:{user_id}:requests"
#     requests_made = redis_client.get(key)
    
#     if requests_made is None:
#         redis_client.set(key, 1, ex=60)  # 1 hour window
#         return False
#     elif int(requests_made) >= 5:
#         return True
#     else:
#         redis_client.incr(key)
#         return False

# # Helper function to convert MongoDB document to JSON serializable
# def convert_objectid_to_str(document):
#     if isinstance(document, dict):
#         document['_id'] = str(document['_id'])
#     return document

# # Function to scrape BBC news
# def scrape_bbc_news(url):
#     response = requests.get(url)
    
#     if response.status_code == 200:
#         html_soup = BeautifulSoup(response.text, 'html.parser')
#         articles = html_soup.find_all('div', {'data-testid': 'card-text-wrapper'})
        
#         dict_list = []
#         for article in articles:
#             title = article.find('h2', {'data-testid': 'card-headline'}).text.strip() if article.find('h2', {'data-testid': 'card-headline'}) else None
#             preview = article.find('p', {'data-testid': 'card-description'}).text.strip() if article.find('p', {'data-testid': 'card-description'}) else None
            
#             if title and preview:
#                 dict_list.append({'title': title, 'content': preview})
        
#         return dict_list
#     return []

# # Function to scrape multiple pages and sections
# def scrape_multiple_pages(base_url, sections, max_articles=20, pages_to_scrape=2):
#     all_titles = set()  # To track unique titles
#     all_articles = []  # To store unique articles
    
#     for section in sections:
#         for page_number in range(1, pages_to_scrape + 1):
#             url = f"{base_url}/{section}?page={page_number}"
#             articles = scrape_bbc_news(url)
            
#             if not articles:
#                 break  # Stop if no articles are found
            
#             for article in articles:
#                 if article['title'] not in all_titles:
#                     all_titles.add(article['title'])
#                     all_articles.append(article)
                    
#                 if len(all_articles) >= max_articles:
#                     return all_articles
            
#             time.sleep(2)  # Sleep to avoid overwhelming the server
    
#     return all_articles

# # Function to update database with scraped articles
# def update_database():
#     base_url = 'https://www.bbc.com/news'
#     sections = ['world', 'uk', 'business', 'politics', 'health', 'education', 'science_and_environment', 'technology', 'entertainment_and_arts']
    
#     news_articles = scrape_multiple_pages(base_url, sections)
    
#     for article in news_articles:
#         title = article['title']
#         preview = article['content']
        
#         if preview:  # Ensure there is content
#             documents_collection.update_one(
#                 {'title': title},
#                 {'$set': {'content': preview}},
#                 upsert=True
#             )

# # Function to update user logs in the database
# def update_user_log(user_id, action):
#     try:
#         users_collection.update_one(
#             {'user_id': user_id},
#             {
#                 '$set': {'last_action': action, 'timestamp': time.time()},
#                 '$inc': {'request_count': 1}  # Increment request count
#             },
#             upsert=True
#         )
#     except Exception as e:
#         app.logger.error(f"Error updating user log: {e}")

# # Background scraper thread
# def scraper_thread_func():
#     while True:
#         try:
#             update_database()
#             time.sleep(3600)  # Scrape every hour
#         except Exception as e:
#             app.logger.error(f"Error scraping articles: {e}")

# # Start the scraper thread
# scraper_thread = threading.Thread(target=scraper_thread_func, daemon=True)
# scraper_thread.start()

# # API endpoint to check if the API is active
# @app.route('/health', methods=['GET'])
# def health():
#     return jsonify({"status": "API is active"}), 200

# # API endpoint for document search
# @app.route('/search', methods=['POST'])
# def search():
#     start_time = time.time()
#     user_id = request.json.get('user_id')
#     if not user_id:
#         return jsonify({'error': 'user_id is required'}), 400

#     if rate_limit(user_id):
#         return jsonify({"error": "Too many requests"}), 429

#     # Update user log
#     update_user_log(user_id, 'Search performed')

#     text = request.json.get('text', '')
#     top_k = int(request.json.get('top_k', 5))
#     threshold = float(request.json.get('threshold', 0.5))

#     cache_key = f"{text}_{top_k}_{threshold}"
#     cached_result = redis_client.get(cache_key)
#     inference_time = time.time() - start_time
    
#     if cached_result:
#         return jsonify({"inference_time": f"{inference_time:.2f}ms", "source": "cache", "results": json.loads(cached_result)}), 200
    
#     results = list(documents_collection.find({'title': {'$regex': text, '$options': 'i'}}).limit(top_k))
#     results = [convert_objectid_to_str(result) for result in results]
    
#     if results:
#         cache_response(cache_key, results)

#     return jsonify({"inference_time": f"{inference_time:.2f}ms", "source": "db", "results": results}), 200

# # API logging and tracking request time
# @app.before_request
# def track_request_time():
#     request.start_time = time.time()

# @app.after_request
# def log_request_time(response):
#     processing_time = time.time() - request.start_time
#     app.logger.info(f"Processed request in {processing_time:.2f} seconds.")
#     return response

# # Main entry point for running the Flask app
# if __name__ == '__main__':
#     app.run(debug=True)


from flask import Flask, request, jsonify
from pymongo import MongoClient
from redis_setup import RedisClient, cache_response, rate_limit
from scraper import update_database
import threading
import time
import json

app = Flask(__name__)

# MongoDB setup
client = MongoClient('mongodb+srv://ananyasundar2004:123@cluster0.tf1ob.mongodb.net/')
db = client['Trade_1414']
users_collection = db['users']
documents_collection = db['Documents']

# Redis setup
redis_client = RedisClient(host='localhost', port=6379, decode_responses=True).client

# Helper function to convert MongoDB document to JSON serializable
def convert_objectid_to_str(document):
    if isinstance(document, dict):
        document['_id'] = str(document['_id'])
    return document

# Function to update user logs in the database
def update_user_log(user_id, action):
    try:
        users_collection.update_one(
            {'user_id': user_id},
            {
                '$set': {'last_action': action, 'timestamp': time.time()},
                '$inc': {'request_count': 1}  # Increment request count
            },
            upsert=True
        )
    except Exception as e:
        app.logger.error(f"Error updating user log: {e}")

# Background scraper thread
def scraper_thread_func():
    while True:
        try:
            update_database()
            time.sleep(3600)  # Scrape every hour
        except Exception as e:
            app.logger.error(f"Error scraping articles: {e}")

# Start the scraper thread
scraper_thread = threading.Thread(target=scraper_thread_func, daemon=True)
scraper_thread.start()

# API endpoint to check if the API is active
@app.route('/health', methods=['GET'])
def health():
    return jsonify({"status": "API is active"}), 200

# API endpoint for document search
@app.route('/search', methods=['POST'])
def search():
    start_time = time.time()
    user_id = request.json.get('user_id')
    if not user_id:
        return jsonify({'error': 'user_id is required'}), 400

    if rate_limit(user_id, redis_client):  # Pass redis_client here
        return jsonify({"error": "Too many requests"}), 429

    # Update user log
    update_user_log(user_id, 'Search performed')

    text = request.json.get('text', '')
    top_k = int(request.json.get('top_k', 5))
    threshold = float(request.json.get('threshold', 0.5))

    cache_key = f"{text}_{top_k}_{threshold}"
    cached_result = redis_client.get(cache_key)
    inference_time = time.time() - start_time
    
    if cached_result:
        return jsonify({"inference_time": f"{inference_time:.2f}ms", "source": "cache", "results": json.loads(cached_result)}), 200
    
    results = list(documents_collection.find({'title': {'$regex': text, '$options': 'i'}}).limit(top_k))
    results = [convert_objectid_to_str(result) for result in results]
    
    if results:
        cache_response(cache_key, results, redis_client)

    return jsonify({"inference_time": f"{inference_time:.2f}ms", "source": "db", "results": results}), 200

# API logging and tracking request time
@app.before_request
def track_request_time():
    request.start_time = time.time()

@app.after_request
def log_request_time(response):
    processing_time = time.time() - request.start_time
    app.logger.info(f"Processed request in {processing_time:.2f} seconds.")
    return response

# Main entry point for running the Flask app
if __name__ == '__main__':
    app.run(debug=True)

