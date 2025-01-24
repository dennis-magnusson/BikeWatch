from typing import List

from fastapi import Depends, FastAPI, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy import create_engine, func, or_
from sqlalchemy.orm import Session, joinedload, sessionmaker

from common import BikeListing, UserAlert

app = FastAPI()

origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

DATABASE_URL = "sqlite:///data/bikes.db"

engine = create_engine("sqlite:///data/bikes.db")
Session = sessionmaker(bind=engine)


def get_db():
    db = Session()
    try:
        yield db
    finally:
        db.close()


@app.get("/listings/")
def get_listings(
    db=Depends(get_db),
    min_price: int = Query(None),
    max_price: int = Query(None),
    city: List[str] = Query(None),
    region: List[str] = Query(None),
    category: List[str] = Query(None),
    sort_by: str = Query("newest"),
    size: float = Query(None),
    size_flexibility: bool = Query(False),
    pagination: int = Query(1),
):
    OFFSET = 30

    if min_price is not None and max_price is not None and max_price < min_price:
        raise HTTPException(
            status_code=400, detail="max_price cannot be smaller than min_price"
        )

    print(f"{min_price=}, {max_price=}")
    query = db.query(BikeListing).options(joinedload(BikeListing.images))

    # Apply filters dynamically
    if min_price:
        query = query.filter(BikeListing.price >= min_price)
    if max_price:
        query = query.filter(BikeListing.price <= max_price)
    if city or region:
        location_filters = []
        if city:
            location_filters.extend(
                [func.lower(BikeListing.city) == c.lower() for c in city]
            )
        if region:
            location_filters.extend(
                [func.lower(BikeListing.region) == r.lower() for r in region]
            )
        query = query.filter(or_(*location_filters))
    if category:
        query = query.filter(BikeListing.category.in_(category))
    if size:
        if size_flexibility:
            query = query.filter(
                (BikeListing.number_size_min <= size + 1)
                & (BikeListing.number_size_max >= size - 1)
            )
        else:
            query = query.filter(
                (BikeListing.number_size_min <= size)
                & (BikeListing.number_size_max >= size)
            )

    # Apply sorting
    if sort_by == "price_inc":
        query = query.order_by(BikeListing.price.asc())
    elif sort_by == "price_dec":
        query = query.order_by(BikeListing.price.desc())
    elif sort_by == "newest":
        query = query.order_by(BikeListing.date_posted.desc())
    elif sort_by == "oldest":
        query = query.order_by(BikeListing.date_posted.asc())

    # Apply pagination and get results
    total = query.count()
    query = query.limit(30).offset(OFFSET * (pagination - 1))
    results = query.all()

    return {"total": total, "listings": results}


@app.get("/locations/")
def get_locations(db=Depends(get_db)):
    # get all unique cities and regions but not null values
    cities = (
        db.query(BikeListing.city).distinct().filter(BikeListing.city.isnot(None)).all()
    )
    regions = (
        db.query(BikeListing.region)
        .distinct()
        .filter(BikeListing.region.isnot(None))
        .all()
    )

    locations = []
    for city in cities:
        locations.append({"locationType": "city", "name": city[0]})
    for region in regions:
        locations.append({"locationType": "region", "name": region[0]})

    locations = sorted(
        locations, key=lambda x: x["name"] != "Uusimaa"
    )  # Sort Uusimaa first always

    return locations


@app.get("/categories/")
def get_categories(db=Depends(get_db)):
    categories = db.query(BikeListing.category).distinct().all()

    # Sort road, gravel and hybrid always first
    categories = sorted(
        categories,
        key=lambda x: x[0] not in ["road", "gravel", "hybrid"],
    )

    return [category[0] for category in categories]


@app.get("/alerts/")
def get_alerts(db: Depends(get_db)):
    alerts = db.query(UserAlert).all()
    return alerts


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)
