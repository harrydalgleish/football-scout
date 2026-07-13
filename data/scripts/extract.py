import requests

def download_competitions():
    url = "https://raw.githubusercontent.com/statsbomb/open-data/refs/heads/master/data/competitions.json"

    response = requests.get(url)

    with open("data/raw/competitions.json", "w") as file:
        file.write(response.text)

def download_matches(competition_id, season_id):
    specific_url = f"https://raw.githubusercontent.com/statsbomb/open-data/refs/heads/master/data/matches/{competition_id}/{season_id}.json"
    specific_file = f"{competition_id}_{season_id}.json"

    response = requests.get(specific_url)

    with open(f"data/raw/matches/{specific_file}", "w") as file:
        file.write(response.text)

def download_events(match_id):
    specific_url = f"https://raw.githubusercontent.com/statsbomb/open-data/refs/heads/master/data/events/{match_id}.json"
    specific_file = f"{match_id}.json"

    response = requests.get(specific_url)

    with open(f"data/raw/events/{specific_file}", "w") as file:
        file.write(response.text)