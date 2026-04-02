from fastapi import APIRouter

router = APIRouter()

@router.get("/", tags=["rooter"])
def root():
    return {'message': "Hi!"}