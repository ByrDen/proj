from fastapi import FastAPI
from shop.handlers.v1 import router as mans_router

app = FastAPI()
app.include_router(router=mans_router)


if __name__ == '__main__':
    from uvicorn import run
    run(
        app=app,
        host="127.0.0.1",
        port=80,
    )
