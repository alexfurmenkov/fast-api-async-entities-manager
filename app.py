from fastapi import FastAPI

from api.routes import auth_router, users_router

app = FastAPI()
app.include_router(auth_router)
app.include_router(users_router)


@app.get("/")
async def root():
    return {"message": "Hello World"}
