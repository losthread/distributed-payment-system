from dotenv import load_dotenv
import redis.asyncio as redis
import os

# lead env variables
load_dotenv()

REDIS_PASSWORD = os.getenv("REDIS_PASSWORD")

# cache
cache = redis.Redis(
  host="redis", 
  port=6379,
  password=REDIS_PASSWORD, 
  decode_responses=True
)