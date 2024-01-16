from fastapi import FastAPI

from Routers.adminRouter import admin_router


app = FastAPI()
app.include_router(admin_router)
