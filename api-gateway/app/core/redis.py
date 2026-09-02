from dotenv import load_dotenv
import redis
import os

# lead env variables
load_dotenv()

REDIS_PASSWORD = os.getenv("REDIS_PASSWORD")

# cache
cache = redis.Redis(
  host="localhost", 
  port=6379,
  password=REDIS_PASSWORD, 
  decode_responses=True
)