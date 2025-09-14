from fastapi import APIRouter, Depends, HTTPException, status
from typing import List
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.models.schemas import cart as cart_schemas

router = APIRouter()


def _get_user_id_from_dep():
    # placeholder dependency - adapt to your auth dependency
    # for now assume user_id=1 for testing; replace with real auth dependency
    return 1


@router.get("/", response_model=cart_schemas.Cart)
def get_cart(db: Session = Depends(get_db), user_id: int = Depends(_get_user_id_from_dep)):
    # load or create cart for user
    row = db.execute("SELECT id FROM public.carts WHERE owner_user_id = %s AND status='active' LIMIT 1", (user_id,)).fetchone()
    if not row:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="cart not found")
    cart_id = row[0]
    items = db.execute(
        """
        SELECT ci.id, ci.product_id, ci.quantity, ci.price_at_add, ci.metadata,
               p.id AS p_id, p.name AS p_title, p.description AS p_description, p.price AS p_price
        FROM public.cart_items ci
        LEFT JOIN public.products p ON p.id = ci.product_id
        WHERE ci.cart_id = %s
        """,
        (cart_id,)
    ).fetchall()
    cart_items = []
    for it in items:
        product = None
        if it[5] is not None:
            product = cart_schemas.ProductRead(id=it[5], title=it[6], description=it[7], price=float(it[8]))
        cart_items.append(cart_schemas.CartItemResponse(item_id=it[0], product_id=it[1], quantity=it[2], price_at_add=float(it[3]), metadata=it[4] or {}, product=product))
    return cart_schemas.Cart(cart_id=cart_id, owner_user_id=user_id, items=cart_items)


@router.post("/items", response_model=cart_schemas.CartItemResponse, status_code=201)
def add_cart_item(payload: cart_schemas.CartItemCreate, db: Session = Depends(get_db), user_id: int = Depends(_get_user_id_from_dep)):
    # ensure cart
    row = db.execute("SELECT id FROM public.carts WHERE owner_user_id = %s AND status='active' LIMIT 1", (user_id,)).fetchone()
    if not row:
        db.execute("INSERT INTO public.carts (owner_user_id) VALUES (%s)", (user_id,))
        cart_id = db.execute("SELECT id FROM public.carts WHERE owner_user_id = %s AND status='active' LIMIT 1", (user_id,)).fetchone()[0]
    else:
        cart_id = row[0]
    # get current price
    prod = db.execute("SELECT id, title, description, price FROM public.products WHERE id=%s", (payload.product_id,)).fetchone()
    if not prod:
        raise HTTPException(status_code=404, detail="product not found")
    price = prod[3]
    # upsert into cart_items
    db.execute("INSERT INTO public.cart_items (cart_id,product_id,quantity,price_at_add,metadata) VALUES (%s,%s,%s,%s,%s) ON CONFLICT (cart_id,product_id) DO UPDATE SET quantity = public.cart_items.quantity + EXCLUDED.quantity", (cart_id,payload.product_id,payload.quantity,price, payload.metadata))
    db.commit()
    it = db.execute("SELECT id,product_id,quantity,price_at_add,metadata FROM public.cart_items WHERE cart_id=%s AND product_id=%s", (cart_id,payload.product_id)).fetchone()
    product = cart_schemas.ProductRead(id=prod[0], title=prod[1], description=prod[2], price=float(prod[3]))
    return cart_schemas.CartItemResponse(item_id=it[0], product_id=it[1], quantity=it[2], price_at_add=float(it[3]), metadata=it[4] or {}, product=product)
# Note: keep the router defined above; no adapter rebind necessary after migration
