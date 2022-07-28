from api import get_team_data, get_team_on_top 
from config import TEAM_ID, YEAR, WEBHOOK_URL, COUNTRY, TEAM_NAME
from db import update_db, get_db_data
from time import sleep

import requests
import datetime
import logging

def main():
    # Pull team data
    team_api_data = get_team_data(TEAM_ID) 
    aim_api_data = get_team_on_top(TEAM_NAME, COUNTRY)
    logging.info("Data pulled from CTFTime")

    # Exfil only the data I want
    team_api_data = extract_team_api_data(team_api_data)

    api_data = merge_data(team_api_data,aim_api_data)

    # Pull the same data from database
    db_data = get_db_data()
    logging.info("Data pulled from database")
    
    # Compare data to check if there is a change
    is_diff = check_diff(api_data, db_data)

    if is_diff:
        logging.info("Database has changed")
        # Update database with new data
        update_db(api_data)
        logging.info("Database updated")

        # Don't want race condition happening after database update
        sleep(5) 

        # Hit webhook of MQCybersec bot to update data on discord server
        hit_webhook("Database updated")
        logging.info("Webhook has been hit")
    else:
        logging.info("Database has not changed")

def merge_data(team_api_data, aim_api_data):
    return {"team": team_api_data, "aim": aim_api_data} 

def check_diff(api_data, db_data):
    return api_data != db_data
    
def extract_team_api_data(team_data):
    country = team_data["country"]
    ww_place = team_data["rating"][YEAR]["rating_place"]
    country_place = team_data["rating"][YEAR]["country_place"]
    rating_points = team_data["rating"][YEAR]["rating_points"]
    team_name = team_data["primary_alias"]

    return {"country":country, "worldwide_place":ww_place, "country_place":country_place, "rating_points":rating_points, "team_name": team_name}

def extract_aim_api_data(team_data):
    country = team_data["country"]
    ww_place = team_data["rating"][YEAR]["rating_place"]
    country_place = team_data["rating"][YEAR]["country_place"]
    rating_points = team_data["rating"][YEAR]["rating_points"]

    return {"country":country, "worldwide_place":ww_place, "country_place":country_place, "rating_points":rating_points}

def hit_webhook(msg):
    requests.post(WEBHOOK_URL, data={"content":f"[{datetime.datetime.now()}] - {msg}","embeds":None,"attachments":[]})

if __name__=="__main__":
    try:
        logging.basicConfig(filename='tracker.log', level=logging.DEBUG, format='%(asctime)s %(message)s', datefmt='%m/%d/%Y %I:%M:%S %p')
        main()
    except Exception as e:
        logging.exception("Something died", exc_info=e)
        hit_webhook("SOMETHING DIED - Don't be lazy and check the logs :)")
