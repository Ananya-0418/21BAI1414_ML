from bs4 import BeautifulSoup
import requests
import time
from mongodb import documents_collection

def scrape_bbc_news(url):
    response = requests.get(url)
    
    if response.status_code == 200:
        html_soup = BeautifulSoup(response.text, 'html.parser')
        articles = html_soup.find_all('div', {'data-testid': 'card-text-wrapper'})
        
        dict_list = []
        for article in articles:
            title = article.find('h2', {'data-testid': 'card-headline'}).text.strip() if article.find('h2', {'data-testid': 'card-headline'}) else None
            preview = article.find('p', {'data-testid': 'card-description'}).text.strip() if article.find('p', {'data-testid': 'card-description'}) else None
            
            if title and preview:
                dict_list.append({'title': title, 'content': preview})
        
        return dict_list
    return []

def scrape_multiple_pages(base_url, sections, max_articles=20, pages_to_scrape=2):
    all_titles = set()  # To track unique titles
    all_articles = []  # To store unique articles
    
    for section in sections:
        for page_number in range(1, pages_to_scrape + 1):
            url = f"{base_url}/{section}?page={page_number}"
            articles = scrape_bbc_news(url)
            
            if not articles:
                break  # Stop if no articles are found
            
            for article in articles:
                if article['title'] not in all_titles:
                    all_titles.add(article['title'])
                    all_articles.append(article)
                    
                if len(all_articles) >= max_articles:
                    return all_articles
            
            time.sleep(2)  # Sleep to avoid overwhelming the server
    
    return all_articles

def update_database():
    base_url = 'https://www.bbc.com/news'
    sections = ['world', 'uk', 'business', 'politics', 'health', 'education', 'science_and_environment', 'technology', 'entertainment_and_arts']
    
    news_articles = scrape_multiple_pages(base_url, sections)
    
    for article in news_articles:
        title = article['title']
        preview = article['content']
        
        if preview:  # Ensure there is content
            documents_collection.update_one(
                {'title': title},
                {'$set': {'content': preview}},
                upsert=True
            )
