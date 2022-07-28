from dotenv import load_dotenv
import os

load_dotenv()

MONGODB_URL=os.getenv("MONGODB_URL")
TEAM_ID=os.getenv("TEAM_ID")
YEAR=os.getenv("YEAR")
COUNTRY=os.getenv("COUNTRY")
WEBHOOK_URL=os.getenv("WEBHOOK_URL")
DATABASE_NAME = os.getenv("DATABASE_NAME")
TEAM_NAME=os.getenv("TEAM_NAME")
CTFTIME_URL=os.getenv("CTFTIME_URL")
USER_AGENT=os.getenv("USER_AGENT")