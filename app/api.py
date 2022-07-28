import requests
from config import YEAR, CTFTIME_URL, USER_AGENT
from bs4 import BeautifulSoup

def get_team_data(id):
    r = send_request(f"{CTFTIME_URL}/api/v1/teams/{id}/")
    return r.json()

def get_team_on_top(target_team, country):
    # Scrape website
    URL = f"{CTFTIME_URL}/stats/{YEAR}/{country}"
    r = send_request(URL)
    soup = BeautifulSoup(r.text, "html.parser")
    rows = soup.find_all("tr")

    prev_team = {}
    for i in rows[1:]:
        cols = i.find_all("td")
        world_place = cols[0].get_text()
        local_place = cols[2].get_text()
        team_name = cols[4].get_text()
        rating = cols[5].get_text()
        if team_name == target_team:
            return prev_team
        
        prev_team["worldwide_place"] = world_place
        prev_team["country_place"] = local_place
        prev_team["team_name"] = team_name 
        prev_team["rating_points"] = rating
        prev_team["country"] = country

    return {}

def send_request(url):
    r = requests.get(url, headers={"User-Agent":USER_AGENT})
    return r
