from fastapi import FastAPI
from threading import Thread
from contextlib import asynccontextmanager
from .kafka import consume_events
from ..routes import wallet
from fastapi.middleware.cors import CORSMiddleware
import uvicorn

# event consumer lifespan
@asynccontextmanager
async def lifespan(app: FastAPI):
  consumer_thread: Thread = Thread(
    target = consume_events,
    daemon = True
  )

  consumer_thread.start()

  yield

# create FastAPI instance - app that uvicorn serves
app: FastAPI = FastAPI(lifespan = lifespan)

# include routers
app.include_router(wallet.router)

# CORS middleware
app.add_middleware(
  CORSMiddleware,
  allow_origins=['http://localhost:5173', 'http://localhost:5174'], # add prod frontend url later
  allow_credentials=True,
  allow_methods=["GET", "POST", "PUT", "DELETE"],
  allow_headers=["Content-Type", "Authorization"],
)

# run server
if __name__ == '__main__':
  print("Welcome to Wallet Microservice version 1.0.0")
  uvicorn.run("app.core.main:app", host = "0.0.0.0", port = 7000, reload = False)