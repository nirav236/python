import os
from flask import Flask, request, render_template
from bs4 import BeautifulSoup
import requests

app = Flask(__name__)

API_KEY = 'AIzaSyDdcmPJRg8ep0-rZEnErJvMT3Gy0xXH_YY'  # Replace with your actual Google API key
CX = '30c09aa5edd914ba4'  # Your provided Search Engine ID

def get_product_info(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')
    title = soup.find('title').get_text()
    description_tag = soup.find('meta', attrs={'name': 'description'})
    description = description_tag['content'] if description_tag else title
    image_tag = soup.find('meta', attrs={'property': 'og:image'})
    image_url = image_tag['content'] if image_tag else None
    return title, description, image_url

def search_similar_products(query, api_key, cx):
    url = f"https://www.googleapis.com/customsearch/v1?q={query}&key={api_key}&cx={cx}"
    response = requests.get(url)
    search_results = response.json()
    return search_results

@app.route('/')
def home():
    # Check if template exists
    if not os.path.exists('templates/index.html'):
        return "Template 'index.html' not found", 404
    return render_template('index.html')

@app.route('/search', methods=['POST'])
def search():
    product_url = request.form['product_url']
    title, description, image_url = get_product_info(product_url)
    query = f"{title} {description}"
    search_results = search_similar_products(query, API_KEY, CX)
    return render_template('result.html', results=search_results, image_url=image_url)

if __name__ == '__main__':
    app.run(debug=True)
