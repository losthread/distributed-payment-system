from fastapi import FastAPI
from .routes import notification
from fastapi.middleware.cors import CORSMiddleware
import uvicorn

# create fastAPI instance - app that uvicorn serves
app: FastAPI = FastAPI()

# include routers
app.include_router(notification.router)

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
  print("Welcome to Notification Microservice version 1.0.0")
  uvicorn.run("app.core.main:app", host = "0.0.0.0", port = 8003, reload = False)