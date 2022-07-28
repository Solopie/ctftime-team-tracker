import requests
from .config import YEAR
from bs4 import BeautifulSoup

CTFTIME_URL = "https://ctftime.org"
USER_AGENT = "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:102.0) Gecko/20100101 Firefox/102.0"

def get_team_data(id):
    r = send_request(f"{CTFTIME_URL}/api/v1/teams/{id}/")
    return r.json()

def get_next_team_data(id):
    pass

def get_country_teams(country):
    # Scrape website
    URL = f"{CTFTIME_URL}/stats/{YEAR}/{country}"
    r = send_request(URL)
    soup = BeautifulSoup(r.text, "html.parser")

    print(soup)

def send_request(url):
    r = requests.get(url, headers={"User-Agent":USER_AGENT})
    return r

get_country_teams("AU")
