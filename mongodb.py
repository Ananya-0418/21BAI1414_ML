# from pymongo import MongoClient
# import time

# client = MongoClient('mongodb+srv://ananyasundar2004:123@cluster0.tf1ob.mongodb.net/')
# db = client['Trade_1414']
# users_collection = db['users']
# documents_collection = db['Documents']

# def convert_objectid_to_str(document):
#     if isinstance(document, dict):
#         document['_id'] = str(document['_id'])
#     return document

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
#         print(f"Error updating user log: {e}")

# def update_database():
#     from scraper import scrape_multiple_pages
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

from pymongo import MongoClient

client = MongoClient('mongodb+srv://ananyasundar2004:123@cluster0.tf1ob.mongodb.net/')
db = client['Trade_1414']
users_collection = db['users']
documents_collection = db['Documents']

def convert_objectid_to_str(document):
    if isinstance(document, dict):
        document['_id'] = str(document['_id'])
    return document
