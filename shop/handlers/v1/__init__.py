from fastapi import APIRouter

from shop.handlers.v1 import mans
from shop.handlers.v1 import departments


router = APIRouter(
    prefix="/v1",
)
router.include_router(router=mans.router)
router.include_router(router=departments.router)
