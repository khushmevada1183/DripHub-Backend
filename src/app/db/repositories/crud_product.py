from sqlalchemy.orm import Session
from app import models
from app.models.schemas.product import ProductCreate


def create_product(db: Session, product_in: ProductCreate):
    # Map legacy incoming fields (title, price) to current product columns
    db_obj = models.product.Product(
        product_name=product_in.title,
        description=product_in.description,
        real_price=product_in.price,
        current_price=product_in.price,
    )
    db.add(db_obj)
    db.commit()
    db.refresh(db_obj)
    return db_obj

def get_product(db: Session, product_id: int):
    return db.query(models.product.Product).filter(models.product.Product.id == product_id).first()

def list_products(db: Session, skip: int = 0, limit: int = 100):
    # Return a merged list: first enriched rows from featured_products,
    # then remaining rows from products (mapped into the same shape).
    from sqlalchemy import text
    results = []
    try:
        feat_rows = db.execute(
            text("SELECT id, product_name, category, rating, people_rated_count, description, img_url, real_price, current_price, created_at FROM public.featured_products ORDER BY id LIMIT :limit OFFSET :skip"),
            {"limit": limit, "skip": skip},
        ).fetchall()
    except Exception:
        feat_rows = []

    feat_ids = set()
    for r in feat_rows:
        feat_ids.add(r[0])
        results.append({
            "id": r[0],
            "product_name": r[1],
            "category": r[2],
            "rating": float(r[3]) if r[3] is not None else None,
            "people_rated_count": int(r[4]) if r[4] is not None else None,
            "description": r[5],
            "img_url": r[6],
            "real_price": float(r[7]) if r[7] is not None else None,
            "current_price": float(r[8]) if r[8] is not None else None,
            "created_at": r[9],
        })

    # Fill up remaining results from products table (exclude featured ids)
    # We fetch up to `limit` rows starting from `skip` but since featured
    # rows were already taken into account we simply query products and
    # append those not in featured set until we reach `limit`.
    try:
        # products table now uses the enriched schema (product_name, real_price, current_price)
        prod_rows = db.execute(text("SELECT id, product_name, description, real_price, current_price, created_at FROM public.products ORDER BY id"), {}).fetchall()
    except Exception:
        prod_rows = []

    for pr in prod_rows:
        if len(results) >= limit:
            break
        pid = pr[0]
        if pid in feat_ids:
            continue
        results.append({
            "id": pid,
            "product_name": pr[1],
            "category": None,
            "rating": None,
            "people_rated_count": None,
            "description": pr[2],
            "img_url": None,
            "real_price": float(pr[3]) if pr[3] is not None else None,
            "current_price": float(pr[3]) if pr[3] is not None else None,
            "created_at": pr[4],
        })

    # Apply skip manually: skip was intended to offset the overall list
    if skip:
        results = results[skip:]
    return results[:limit]


def list_featured_products(db: Session, skip: int = 0, limit: int = 100):
    # Use raw SQL to read from the featured_products table which may have
    # different column names and is not modeled as an ORM class in this
    # codebase.
    from sqlalchemy import text
    rows = db.execute(
        text("SELECT id, product_name, category, rating, people_rated_count, description, img_url, real_price, current_price, created_at FROM public.featured_products ORDER BY id LIMIT :limit OFFSET :skip"),
        {"limit": limit, "skip": skip},
    ).fetchall()
    return rows
