import requests

# url = "https://simple-books-api.glitch.me/books"
url = "https://netpacklogistic.com/api/measurement-entries"

payload={}
headers = {}

response = requests.request("GET", url, headers=headers, data=payload)

print(response.text)
