from .api import get_team_data , get_next_team_data
from .config import TEAM_ID, YEAR, WEBHOOK_URL
from .db import update_db, get_db_data
from time import sleep

import requests

def main():
    # Pull team data
    team_api_data = get_team_data(TEAM_ID) 
    aim_api_data = get_next_team_data(TEAM_ID)

    # Exfil only the data I want
    team_api_data = extract_team_api_data(team_api_data)
    aim_api_data = extract_aim_api_data(aim_api_data)

    api_data = merge_data(team_api_data,aim_api_data)

    # Pull the same data from database
    db_data = get_db_data()
    
    # Compare data to check if there is a change
    is_diff = check_diff(api_data, db_data)

    if is_diff:
        # Update database with new data
        update_db(api_data)

        # Don't want race condition happening after database update
        sleep(60) 

        # Hit webhook of MQCybersec bot to update data on discord server
        requests.get(WEBHOOK_URL)
        pass
    

def merge_data(team_api_data, aim_api_data):
    
    pass

def check_diff(api_data, db_data):
    print(api_data.__dict__.items() ^ db_data.__dict__.items())
    return False
    
def extract_team_api_data(team_data):
    country = team_data["country"]
    ww_place = team_data["rating"][YEAR]["rating_place"]
    country_place = team_data["rating"][YEAR]["country_place"]
    rating_points = team_data["rating"][YEAR]["rating_points"]

    return {"country":country, "worldwide_place":ww_place, "country_place":country_place, "rating_points":rating_points}

def extract_aim_api_data(team_data):
    country = team_data["country"]
    ww_place = team_data["rating"][YEAR]["rating_place"]
    country_place = team_data["rating"][YEAR]["country_place"]
    rating_points = team_data["rating"][YEAR]["rating_points"]

    return {"country":country, "worldwide_place":ww_place, "country_place":country_place, "rating_points":rating_points}




if __name__=="__main__":
    main()
