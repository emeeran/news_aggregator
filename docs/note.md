GET /news/23 HTTP/1.1
X-Rapidapi-Key: df746a2329msh00ca6a597237acdp1d89cajsnf2d16f69bbc0
X-Rapidapi-Host: the-hindu-national-news.p.rapidapi.com
Host: the-hindu-national-news.p.rapidapi.com


import http.client

conn = http.client.HTTPSConnection("the-hindu-national-news.p.rapidapi.com")

headers = {
    'x-rapidapi-key': "df746a2329msh00ca6a597237acdp1d89cajsnf2d16f69bbc0",
    'x-rapidapi-host': "the-hindu-national-news.p.rapidapi.com"
}

conn.request("GET", "/news/23", headers=headers)

res = conn.getresponse()
data = res.read()

print(data.decode("utf-8"))