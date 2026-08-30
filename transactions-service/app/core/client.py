import httpx

client = httpx.AsyncClient(
  timeout=10.0,
  follow_redirects=True
)