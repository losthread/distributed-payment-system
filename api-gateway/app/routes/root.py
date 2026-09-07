from fastapi import APIRouter

# instantiate API router
router: APIRouter = APIRouter()

@router.get("/")
async def root() -> str:
  return "API Gateway is running!"