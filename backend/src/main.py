from typing import List

from fastapi import Depends, FastAPI, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy import create_engine, func, or_
from sqlalchemy.orm import Session, joinedload, sessionmaker

from common.models import BikeListing

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
    minPrice: int = Query(None),
    maxPrice: int = Query(None),
    city: List[str] = Query(None),
    region: List[str] = Query(None),
    sortBy: str = Query("newest")
):
    if minPrice is not None and maxPrice is not None and maxPrice < minPrice:
        raise HTTPException(status_code=400, detail="maxPrice cannot be smaller than minPrice")
    
    print(f"{minPrice=}, {maxPrice=}")
    query = db.query(BikeListing).options(joinedload(BikeListing.images))

    # Apply filters dynamically
    if minPrice is not None:
        query = query.filter(BikeListing.price >= minPrice)
    if maxPrice is not None:
        query = query.filter(BikeListing.price <= maxPrice)
    if city or region:
        location_filters = []
        if city:
            location_filters.extend([func.lower(BikeListing.city) == c.lower() for c in city])
        if region:
            location_filters.extend([func.lower(BikeListing.region) == r.lower() for r in region])
        query = query.filter(or_(*location_filters))

    # Apply sorting
    if sortBy == "price_inc":
        query = query.order_by(BikeListing.price.asc())
    elif sortBy == "price_dec":
        query = query.order_by(BikeListing.price.desc())
    elif sortBy == "newest":
        query = query.order_by(BikeListing.date_posted.desc())
    elif sortBy == "oldest":
        query = query.order_by(BikeListing.date_posted.asc())

    # Execute query
    results = query.all()

    return results

@app.get("/locations/")
def get_locations(db=Depends(get_db)):
    cities = db.query(BikeListing.city).distinct().all()
    regions = db.query(BikeListing.region).distinct().all()

    locations = []
    for city in cities:
        locations.append({"locationType": "city", "name": city[0]})
    for region in regions:
        locations.append({"locationType": "region", "name": region[0]})

    locations = sorted(locations, key=lambda x: x["name"] != "Uusimaa") # Sort Uusimaa first always

    return locations

if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)
