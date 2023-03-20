from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from app.api.controller import controller

app = FastAPI(openapi_url="/api/v1/controller/openapi.json",
              docs_url="/api/v1/controller/docs")

app.mount("/api/v1/controller/static", StaticFiles(directory="app/static"),
          name="static")

app.include_router(controller, prefix='/api/v1/controller',
                   tags=['controller'])
