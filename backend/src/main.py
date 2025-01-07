from typing import List

from fastapi import Depends, FastAPI, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy import create_engine, func
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
    location: List[str] = Query(None),
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
    if location:
        for location in location:
            if location.startswith("city_"):
                city_name = location[len("city_"):].lower()
                query = query.filter(func.lower(BikeListing.city) == city_name)
            else: # location.startswith("region_") is True
                region_name = location[len("region_"):].lower()
                query = query.filter(func.lower(BikeListing.region) == region_name)

    # Execute query
    results = query.all()


    return results

@app.get("/locations/")
def get_locations(db=Depends(get_db)):
    cities = db.query(BikeListing.city).distinct().all()
    regions = db.query(BikeListing.region).distinct().all()

    locations = []
    for city in cities:
        locations.append({"value": f"city_{city[0].lower()}", "label": city[0]})
    for region in regions:
        locations.append({"value": f"region_{region[0].lower()}", "label": region[0]})

    locations = sorted(locations, key=lambda x: x["label"] != "Uusimaa") # Sort Uusimaa first always

    return locations

if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)
