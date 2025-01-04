from fastapi import Depends, FastAPI
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy import create_engine
from sqlalchemy.orm import Session, sessionmaker
from sqlalchemy.sql.expression import text

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
def get_listings(db=Depends(get_db)):
    query = """
    SELECT bikes.id, bikes.title, bikes.url, bike_images.image_url, bikes.date_last_updated, bikes.date_posted, bikes.region, bikes.city, bikes.price, bikes.size, bikes.description
    FROM bikes
    LEFT JOIN bike_images ON bikes.id = bike_images.bike_id
    """
    result = db.execute(text(query)).fetchall()

    listings = {}
    for row in result:
        bike_id = row[0]
        if bike_id not in listings:
            listings[bike_id] = {
                "id": bike_id,
                "title": row[1],
                "url": row[2],
                "images": [],
                "last_updated": row[4],
                "originally_posted": row[5],
                "region": row[6],
                "city": row[7],
                "price": row[8],
                "size": row[9],
                "description": row[10],
            }
        listings[bike_id]["images"].append(row[3])

    return list(listings.values())


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)
