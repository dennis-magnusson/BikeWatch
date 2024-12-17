from fastapi import FastAPI

app = FastAPI()


@app.get("/listings/")
def get_listings():
    return []


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)
