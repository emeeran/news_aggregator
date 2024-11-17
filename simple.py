import requests

# Replace with your actual API key
NEWS_API_KEY = "r4swYC56!3KbH&ZFSvmJlq8UM9%"
NEWS_API_URL = "https://newsapi.org/v2/everything"
topic = "Technology"  # or any topic of your choice

params = {"q": topic, "apiKey": NEWS_API_KEY, "language": "en", "pageSize": 5}

response = requests.get(NEWS_API_URL, params=params)

if response.status_code == 200:
    news_data = response.json()
    print("News fetched successfully:", news_data)
else:
    print(f"Error fetching news: {response.status_code}")
