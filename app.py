from flask import Flask, render_template, request, jsonify
from datetime import datetime
import requests
import html
import re
from concurrent.futures import ThreadPoolExecutor

app = Flask(__name__)

# API Keys and URLs
NEWS_API_KEY = "d2b4ffeb2bc14b02b97a2279d4d5628b"
NEWS_API_URL = "https://newsapi.org/v2/everything"


def get_summary(text, num_lines=15):
    if not text:
        return ""

    text = clean_html(text)
    text = re.sub(r"\s+", " ", text).strip()
    text = re.sub(r"\[.*?\]", "", text)

    sentences = re.split(r"[.!?]+", text)
    sentences = [s.strip() for s in sentences if s.strip()]

    summary_sentences = []
    for sent in sentences:
        if len(summary_sentences) >= num_lines:
            break
        if len(sent.split()) > 5:
            summary_sentences.append(sent)

    summary = ". ".join(summary_sentences)
    if summary:
        summary += "."

    return summary


def clean_html(text):
    """Cleans HTML entities and tags from the given text."""
    if not text:
        return ""
    text = html.unescape(text)
    text = re.sub(r"<[^>]+>", "", text)
    return text


def get_news_api_articles(topic):
    """Fetches news articles from the News API based on the given topic."""
    params = {
        "q": topic,
        "apiKey": NEWS_API_KEY,
        "language": "en",
        "pageSize": 25,
        "sortBy": "publishedAt",
    }

    try:
        response = requests.get(NEWS_API_URL, params=params)
        response.raise_for_status()
        news_data = response.json()

        processed_articles = []
        for article in news_data.get("articles", []):
            content = article.get("content", "")
            description = article.get("description", "")
            full_text = f"{description} {content}".strip()

            processed_article = {
                "title": clean_html(article.get("title", "")),
                "url": article.get("url", ""),
                "source": article.get("source", {}).get("name", "Unknown"),
                "published_at": format_date(article.get("publishedAt", "")),
                "summary": get_summary(full_text),
                "image_url": article.get("urlToImage", ""),
                "author": article.get("author", "Unknown"),
                "category": "General News",
            }

            if (
                processed_article["title"]
                and processed_article["url"]
                and processed_article["summary"]
            ):
                processed_articles.append(processed_article)

        return processed_articles
    except requests.exceptions.RequestException as e:
        print(f"Error fetching news: {e}")
        return []


def merge_and_sort_news(topic_news):
    """Merges news articles and sorts them by date."""
    all_news = topic_news
    return sorted(all_news, key=lambda x: x.get("published_at", ""), reverse=True)


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
            # Fetch only from News API
            topic_news = get_news_api_articles(topic)

            news_articles = merge_and_sort_news(topic_news)

            if not news_articles:
                error_message = f"No news found for topic: {topic}"

    return render_template(
        "index.html",
        default_topics=default_topics,
        news_articles=news_articles,
        error_message=error_message,
        selected_topic=selected_topic,
    )


@app.route("/refresh", methods=["GET"])
def refresh_news():
    """Endpoint to refresh news articles."""
    try:
        default_topic = "Technology"

        topic_news = get_news_api_articles(default_topic)

        news_articles = merge_and_sort_news(topic_news)

        return jsonify({"news_articles": news_articles}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500


def format_date(date_str):
    """Formats the given date string to a more readable format."""
    if not date_str:
        return ""
    try:
        # Handle different date formats
        for fmt in ["%Y-%m-%dT%H:%M:%SZ", "%Y-%m-%d %H:%M:%S", "%Y-%m-%d"]:
            try:
                date_obj = datetime.strptime(date_str, fmt)
                return date_obj.strftime("%B %d, %Y %I:%M %p")
            except ValueError:
                continue
        return date_str
    except Exception:  # Changed from bare except
        return date_str


if __name__ == "__main__":
    app.run(debug=False, use_reloader=False)
