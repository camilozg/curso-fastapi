from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles

from routers import jwt_auth, products, users, users_db

app = FastAPI()

# Curso de PYTHON desde CERO para BACKEND: https://youtu.be/_y9qQZXE24A?si=U4_Gz1Yh-J7T1ZVY
# Run server: uvicorn main:app --reload
# Local URL: http://127.0.0.1:8000
# Interactive API docs (Swagger): http://127.0.0.1:8000/docs

# Routers
app.include_router(users_db.router)
# app.include_router(basic_auth.router)
app.include_router(jwt_auth.router)
app.include_router(products.router)
app.include_router(users.router)
app.mount("/static", StaticFiles(directory="static"), name="static")


@app.get("/")
async def root():
    return {"message": "Hello, world!"}
