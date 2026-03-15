from fastapi import APIRouter, HTTPException

router = APIRouter(prefix="/items", tags=["items"])

# имитация БД
items_db = {
    1: {"name": "Laptop", "price": 999.99},
    2: {"name": "Book", "price": 29.99},
    3: {"name": "Pen", "price": 1.99},
}


@router.get("/")
async def list_items():
    """
    Получить список всех товаров.
    """
    return {"items": items_db}


@router.get("/{item_id}")
async def get_item(item_id: int):
    """
    Получить товар по его ID

    Args:
        item_id: ID товара
    """
    if item_id in items_db:
        return {"item_id": item_id, **items_db[item_id]}
    raise HTTPException(status_code=404, detail="Item not found")


@router.post("/{item_id}")
async def update_item(item_id: int, name: str = None, price: float = None):
    """
    Обновить товар.

    Args:
        item_id: ID товара
        name: Новое название (опционально)
        price: Новая цена (опционально)
    """
    if item_id not in items_db:
        raise HTTPException(status_code=404, detail="Item not found")

    if name:
        items_db[item_id]["name"] = name
    if price:
        items_db[item_id]["price"] = price

    return {"item_id": item_id, **items_db[item_id], "message": "Item updated successfully"}
