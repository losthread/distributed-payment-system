from fastapi.middleware.cors import CORSMiddleware
from ..routes import transactions
from fastapi import FastAPI
import uvicorn

# create FastAPI instance - app that uvicorn serves
app: FastAPI = FastAPI()

# include routers
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
if __name__ == '__main__':
  print("Welcome to Transactions Microservice version 1.0.0")
  uvicorn.run("app.core.main:app", host = "0.0.0.0", port = 7000, reload = False)