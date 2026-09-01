from fastapi import FastAPI
from ..routes import auth, wallets, transactions
from fastapi.middleware.cors import CORSMiddleware
import uvicorn

# create fastAPI instance - app tha gunicorn serves
app: FastAPI = FastAPI()

app.include_router(auth.router)
app.include_router(wallets.router)
app.include_router(transactions.router)

# CORS middleware
app.add_middleware(
  CORSMiddleware,
  allow_origins=['http://localhost:5173', 'http://localhost:5174'], # add prod frontend url later
  allow_credentials=True,
  allow_methods=["GET", "POST", "PUT", "DELETE"],
  allow_headers=["Content-Type", "Authorization"],
)

# run server
if __name__ == "__main__":
  print("Welcome to Auth Microservice version 0.1.0")
  uvicorn.run("app.core.main:app", host = "0.0.0.0", port = 8000, reload = False)