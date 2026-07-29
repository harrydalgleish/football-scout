import json

def load_competitions():
    with open("data/raw/competitions.json","r") as file:
        return json.load(file)