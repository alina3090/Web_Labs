from fastapi import FastAPI

from Routers.routers import router


main = FastAPI()
main.include_router(router)
