from dotenv import load_dotenv
import psycopg
import os

# load env variables
load_dotenv()

# get DB URL
DATABASE_URL = os.getenv("DATABASE_URL")

# establish DB connection
conn = psycopg.connect(DATABASE_URL)