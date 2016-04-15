import requests
from config import api
import json

def url_to_name(url):
    parts = url.split("-")
    return " ".join(parts)

def request_new_data():
    url = "https://api.jcdecaux.com/vls/v1/stations?contract=Dublin&apiKey=" + api.API_KEY
    req = requests.get(url)

    parsed_json = json.loads(req.text)
    return parsed_json