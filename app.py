from flask import Flask, request, Response
from goose3 import Goose
from flask_cors import CORS  # Import CORS
app = Flask(__name__)
CORS(app)
def fetch_article_content(url):
    """Fetches and cleans the article content from a given URL.

    Args:
        url: The URL of the news article.

    Returns:
        The cleaned text content of the article or None if extraction fails.
    """
    g = Goose()
    article = g.extract(url=url)
    text = article.cleaned_text
    return text.strip() if text else None

@app.route('/extract', methods=['POST'])
def extract_text():
    data = request.get_json()
    url = data.get('url')
    
    if not url:
        return Response("No URL provided", status=400, mimetype='text/plain')
    
    article_text = fetch_article_content(url)
    
    if article_text:
        return Response(article_text, mimetype='text/plain')
    else:
        return Response("Failed to extract text", status=500, mimetype='text/plain')

if __name__ == '__main__':
    app.run(debug=True)
