from fastapi import FastAPI

from Routers.adminRouter import admin_router
from Routers.adminRouter2 import admin_router2


app = FastAPI()

app.include_router(admin_router)
app.include_router(admin_router2)
