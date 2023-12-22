from fastapi import FastAPI

from routers import products, users

app = FastAPI()

# Run server: uvicorn main:app --reload
# Local URL: http://127.0.0.1:8000
# Interactive API docs (Swagger): http://127.0.0.1:8000/docs

# Routers
app.include_router(products.router)
app.include_router(users.router)


@app.get("/")
async def root():
    return {"message": "Hello, world!"}
