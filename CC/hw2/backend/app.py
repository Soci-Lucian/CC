from flask import Flask, request, jsonify
from flask_cors import CORS
import requests

app = Flask(__name__)
CORS(app)

API_URL = "http://localhost:5000/books"
WIKIPEDIA_API_URL = "https://en.wikipedia.org/w/api.php"
OPENWEATHERMAP_API_KEY = "be6019b7fc7f05b7320317caa255f5b5"
OPENWEATHERMAP_API_URL = "https://api.openweathermap.org/data/2.5/weather"

@app.route('/weather', methods=['GET'])
def get_weather():
    city = request.args.get('city', 'London')
    params = {
        'q': city,
        'appid': OPENWEATHERMAP_API_KEY,
        'units': 'metric' 
    }
    response = requests.get(OPENWEATHERMAP_API_URL, params=params)
    if response.status_code == 200:
        weather_data = response.json()
        return jsonify({
            'city': weather_data['name'],
            'temperature': weather_data['main']['temp'],
            'description': weather_data['weather'][0]['description']
        }), 200
    else:
        return jsonify({'error': 'Failed to fetch weather data'}), response.status_code

def fetch_wikipedia_info(title):
    """Fetch a short summary from Wikipedia based on the book title."""
    
    #Search Wikipedia for the title
    search_params = {
        "action": "query",
        "format": "json",
        "list": "search",
        "srsearch": title
    }
    
    search_response = requests.get(WIKIPEDIA_API_URL, params=search_params)
    search_data = search_response.json()

    if "query" not in search_data or not search_data["query"]["search"]:
        return {"summary": "No Wikipedia page found.", "wikipedia_url": None}

    # first search result's title
    first_result_title = search_data["query"]["search"][0]["title"]

    # summary from Wikipedia
    summary_params = {
        "action": "query",
        "format": "json",
        "prop": "extracts",
        "exintro": True,
        "explaintext": True,
        "titles": first_result_title
    }
    
    summary_response = requests.get(WIKIPEDIA_API_URL, params=summary_params)
    summary_data = summary_response.json()
    
    pages = summary_data.get("query", {}).get("pages", {})
    first_page = next(iter(pages.values()), {})

    if "extract" not in first_page:
        return {"summary": "No summary available.", "wikipedia_url": None}

    return {
        "summary": first_page["extract"],
        "wikipedia_url": f"https://en.wikipedia.org/wiki/{first_result_title.replace(' ', '_')}"
    }

@app.route('/books', methods=['GET', 'POST', 'DELETE'])
def handle_books():
    if request.method == 'GET':
        response = requests.get(API_URL)
        return jsonify(response.json()), response.status_code
    elif request.method == 'POST':
        data = request.json
        response = requests.post(API_URL, json=data)
        return jsonify(response.json()), response.status_code
    elif request.method == 'DELETE':
        response = requests.delete(API_URL)
        return jsonify(response.json()), response.status_code

@app.route('/books/<int:book_id>', methods=['GET', 'PUT', 'DELETE'])
def handle_book(book_id):
    if request.method == 'GET':
        response = requests.get(f"{API_URL}/{book_id}")
        return jsonify(response.json()), response.status_code
    elif request.method == 'PUT':
        data = request.json
        response = requests.put(f"{API_URL}/{book_id}", json=data)
        return jsonify(response.json()), response.status_code
    elif request.method == 'DELETE':
        response = requests.delete(f"{API_URL}/{book_id}")
        return jsonify(response.json()), response.status_code

@app.route('/book-info/<int:book_id>', methods=['GET'])
def get_book_info(book_id):
    """Fetches book info from Wikipedia."""
    response = requests.get(f"{API_URL}/{book_id}")
    if response.status_code != 200:
        return jsonify({"error": f"Book with ID {book_id} not found"}), 404

    book = response.json()
    title = book.get("title", "")
    
    if not title:
        return jsonify({"error": "Book title missing"}), 400

    wikipedia_data = fetch_wikipedia_info(title)
    
    return jsonify({
        "book_id": book_id,
        "title": title,
        "author": book.get("author", ""),
        "summary": wikipedia_data["summary"],
        "wikipedia_url": wikipedia_data["wikipedia_url"]
    })

if __name__ == '__main__':
    app.run(port=8000, debug=True)
