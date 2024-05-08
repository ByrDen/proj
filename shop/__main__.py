from fastapi import FastAPI
from starlette.middleware.gzip import GZipMiddleware
from uvicorn.middleware.proxy_headers import ProxyHeadersMiddleware

from shop.handlers.v1 import router as mans_router

app = FastAPI()
app.add_middleware(middleware_class=GZipMiddleware)
app.add_middleware(middleware_class=ProxyHeadersMiddleware, trusted_hosts=("*", ))


app.include_router(router=mans_router)


if __name__ == '__main__':
    from uvicorn import run
    run(
        app=app,
        host="0.0.0.0",
        port=80,
    )
