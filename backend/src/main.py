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
    city: str = Query(None),
    region: str = Query(None)
):
    if minPrice is not None and maxPrice is not None and maxPrice < minPrice:
        raise HTTPException(status_code=400, detail="maxPrice cannot be smaller than minPrice")
    
    print(f"{minPrice=}, {maxPrice=}, {city=}, {region=}")
    query = db.query(BikeListing).options(joinedload(BikeListing.images))

    # Apply filters dynamically
    if minPrice is not None:
        query = query.filter(BikeListing.price >= minPrice)
    if maxPrice is not None:
        query = query.filter(BikeListing.price <= maxPrice)
    if city is not None:
        query = query.filter(func.lower(BikeListing.city) == city.lower())
    if region is not None:
        query = query.filter(func.lower(BikeListing.region) == region.lower())

    # Execute query
    results = query.all()


    return results

if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)
