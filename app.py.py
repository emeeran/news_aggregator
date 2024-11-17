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
HINDU_API_URL = "https://the-hindu-national-news.p.rapidapi.com/api/news"
HINDU_API_KEY = "YOUR_RAPIDAPI_KEY"  # Replace with your RapidAPI key

HINDU_HEADERS = {
    "X-RapidAPI-Key": HINDU_API_KEY,
    "X-RapidAPI-Host": "the-hindu-national-news.p.rapidapi.com",
}


def get_summary(text, num_lines=5):
    """Generate a 5-line summary from the text."""
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
        if len(sent.split()) > 3:
            summary_sentences.append(sent)

    summary = ". ".join(summary_sentences)
    if summary:
        summary += "."

    return summary


def clean_html(text):
    """Clean HTML entities and tags from text."""
    if not text:
        return ""
    text = html.unescape(text)
    text = re.sub(r"<[^>]+>", "", text)
    return text


def get_hindu_news():
    """Fetch news from The Hindu API."""
    try:
        response = requests.get(HINDU_API_URL, headers=HINDU_HEADERS)
        response.raise_for_status()
        hindu_data = response.json()

        processed_articles = []
        for article in hindu_data.get("data", []):
            processed_article = {
                "title": clean_html(article.get("title", "")),
                "url": article.get("url", ""),
                "source": "The Hindu",
                "published_at": format_date(article.get("published_date", "")),
                "summary": get_summary(article.get("description", "")),
                "image_url": article.get("image_url", ""),
                "author": article.get("author", "The Hindu"),
                "category": "Hindu News",
            }

            if processed_article["title"] and processed_article["url"]:
                processed_articles.append(processed_article)

        return processed_articles
    except requests.exceptions.RequestException as e:
        print(f"Error fetching The Hindu news: {e}")
        return []


def get_news_api_articles(topic):
    """Fetch news from News API."""
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


def merge_and_sort_news(topic_news, hindu_news):
    """Merge and sort news articles by date."""
    all_news = topic_news + hindu_news
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
            # Use ThreadPoolExecutor to fetch from both APIs concurrently
            with ThreadPoolExecutor(max_workers=2) as executor:
                topic_future = executor.submit(get_news_api_articles, topic)
                hindu_future = executor.submit(get_hindu_news)

                topic_news = topic_future.result()
                hindu_news = hindu_future.result()

            news_articles = merge_and_sort_news(topic_news, hindu_news)

            if not news_articles:
                error_message = f"No news found for topic: {topic}"

    return render_template(
        "index.html",
        default_topics=default_topics,
        news_articles=news_articles,
        error_message=error_message,
        selected_topic=selected_topic,
    )


def format_date(date_str):
    """Format the date string to a more readable format."""
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
    except:
        return date_str


if __name__ == "__main__":
    app.run(debug=True)
