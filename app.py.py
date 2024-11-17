from flask import Flask, render_template, request, jsonify
from datetime import datetime
import requests
import html

app = Flask(__name__)

NEWS_API_KEY = "d2b4ffeb2bc14b02b97a2279d4d5628b"
NEWS_API_URL = "https://newsapi.org/v2/everything"


def get_summary(text, max_words=30):
    """Generate a concise summary from the text."""
    if not text:
        return ""
    words = text.split()
    return " ".join(words[:max_words]) + ("..." if len(words) > max_words else "")


def clean_html(text):
    """Clean HTML entities from text."""
    return html.unescape(text) if text else ""


@app.route("/", methods=["GET", "POST"])
def home():
    default_topics = [
        "Technology",
        "Health",
        "Sports",
        "Business",
        "Science",
        "Entertainment",
        "Politics",
        "Environment",
    ]
    news_articles = []
    error_message = None
    selected_topic = ""

    if request.method == "POST":
        topic = request.form.get("topic", "").strip()
        if not topic:
            topic = request.form.get("custom_topic", "").strip()

        if topic:
            selected_topic = topic
            news_articles = get_news_for_topic(topic)
            if not news_articles:
                error_message = f"No news found for topic: {topic}"

    return render_template(
        "index.html",
        default_topics=default_topics,
        news_articles=news_articles,
        error_message=error_message,
        selected_topic=selected_topic,
    )


def get_news_for_topic(topic):
    """Fetch and process news articles based on the selected topic."""
    params = {
        "q": topic,
        "apiKey": NEWS_API_KEY,
        "language": "en",
        "pageSize": 10,
        "sortBy": "publishedAt",
    }

    try:
        response = requests.get(NEWS_API_URL, params=params)
        response.raise_for_status()
        news_data = response.json()

        processed_articles = []
        for article in news_data.get("articles", []):
            # Get the content or description for summary
            content = article.get("content", article.get("description", ""))
            summary = get_summary(clean_html(content))

            # Process the article data
            processed_article = {
                "title": clean_html(article.get("title", "")),
                "url": article.get("url", ""),
                "source": article.get("source", {}).get("name", "Unknown"),
                "published_at": format_date(article.get("publishedAt", "")),
                "summary": summary,
                "image_url": article.get("urlToImage", ""),
                "author": article.get("author", "Unknown"),
            }

            # Only add articles with valid titles and URLs
            if processed_article["title"] and processed_article["url"]:
                processed_articles.append(processed_article)

        return processed_articles
    except requests.exceptions.RequestException as e:
        print(f"Error fetching news: {e}")
        return []


def format_date(date_str):
    """Format the date string to a more readable format."""
    try:
        date_obj = datetime.strptime(date_str, "%Y-%m-%dT%H:%M:%SZ")
        return date_obj.strftime("%B %d, %Y %I:%M %p")
    except:
        return date_str


if __name__ == "__main__":
    app.run(debug=True)
