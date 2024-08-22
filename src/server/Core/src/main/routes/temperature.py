from fastapi import APIRouter

router = APIRouter(
  prefix="/temperature",
  tags=["Temperature"]
)

@router.get("/", status_code=200)
def get_temperature():
  return {"temperature": 25}