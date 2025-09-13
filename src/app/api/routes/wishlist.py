from fastapi import APIRouter, Depends, HTTPException, status
from typing import List
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.models.schemas import wishlist as wl_schemas

router = APIRouter()


def _get_user_id_from_dep():
    # placeholder dependency - adapt to your auth dependency
    return 1


@router.get("/", response_model=List[wl_schemas.WishlistItemResponse])
def get_wishlist(db: Session = Depends(get_db), user_id: int = Depends(_get_user_id_from_dep)):
    row = db.execute("SELECT id FROM public.wishlists WHERE user_id=%s LIMIT 1", (user_id,)).fetchone()
    if not row:
        raise HTTPException(status_code=404, detail="wishlist not found")
    wishlist_id = row[0]
    items = db.execute("SELECT id,product_id,added_at,note FROM public.wishlist_items WHERE wishlist_id=%s ORDER BY added_at DESC", (wishlist_id,)).fetchall()
    return [wl_schemas.WishlistItemResponse(item_id=i[0], product_id=i[1], added_at=i[2], note=i[3]) for i in items]


@router.post("/items", response_model=wl_schemas.WishlistItemResponse, status_code=201)
def add_wishlist_item(payload: wl_schemas.WishlistItemCreate, db: Session = Depends(get_db), user_id: int = Depends(_get_user_id_from_dep)):
    row = db.execute("SELECT id FROM public.wishlists WHERE user_id=%s LIMIT 1", (user_id,)).fetchone()
    if not row:
        db.execute("INSERT INTO public.wishlists (user_id,name) VALUES (%s,%s)", (user_id, 'Default'))
        wishlist_id = db.execute("SELECT id FROM public.wishlists WHERE user_id=%s LIMIT 1", (user_id,)).fetchone()[0]
    else:
        wishlist_id = row[0]
    db.execute("INSERT INTO public.wishlist_items (wishlist_id,product_id,note) VALUES (%s,%s,%s) ON CONFLICT DO NOTHING", (wishlist_id, payload.product_id, payload.note))
    db.commit()
    it = db.execute("SELECT id,product_id,added_at,note FROM public.wishlist_items WHERE wishlist_id=%s AND product_id=%s", (wishlist_id, payload.product_id)).fetchone()
    return wl_schemas.WishlistItemResponse(item_id=it[0], product_id=it[1], added_at=it[2], note=it[3])
