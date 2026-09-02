from fastapi import FastAPI, Request, Response, status
from fastapi.middleware.cors import CORSMiddleware
from ..routes import auth, wallets, transactions
from ..services.ratelimiter import rate_limit
import uvicorn

# create fastAPI instance - app tha gunicorn serves
app: FastAPI = FastAPI()

app.include_router(auth.router)
app.include_router(wallets.router)
app.include_router(transactions.router)

# IP logging middleware for rate limiting
@app.middleware("http")
async def rate_limit_middleware(request: Request, call_next):
  ip = request.client.host

  # if limit exceeds raise 429
  if not await rate_limit(ip):
    return Response(status_code = status.HTTP_429_TOO_MANY_REQUESTS)

  return await call_next

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