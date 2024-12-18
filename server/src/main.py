from fastapi import FastAPI, Depends
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session
from sqlalchemy.sql.expression import text

app = FastAPI()

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
def get_listings(db: Session = Depends(get_db)):
    query = """
    SELECT bikes.id, bikes.title, bikes.url, bike_images.image_url
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
            }
        listings[bike_id]["images"].append(row[3])

    return list(listings.values())


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)
