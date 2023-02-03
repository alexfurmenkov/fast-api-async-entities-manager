from fastapi import FastAPI

from api.routes import users_router

app = FastAPI()
app.include_router(users_router)


@app.get("/")
async def root():
    return {"message": "Hello World"}
