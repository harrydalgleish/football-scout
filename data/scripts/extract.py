import requests

url = "https://raw.githubusercontent.com/statsbomb/open-data/refs/heads/master/data/competitions.json"

response = requests.get(url)

with open("data/raw/competitions.json", "w") as file:
    file.write(response.text)