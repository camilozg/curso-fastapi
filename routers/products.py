from fastapi import APIRouter

router = APIRouter(
    prefix="/products",
    tags=["products"],
)

products_list = ["P0", "P1", "P2", "P3", "P4", "P5"]


@router.get("/")
async def get_all_products():
    return products_list


@router.get("/{id}")
async def get_product(id: int):
    return products_list[id]
