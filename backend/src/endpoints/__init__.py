"""Routers class"""
from fastapi.applications import FastAPI
from .routers import router as main_router

def include_all_routers(app: FastAPI, handler, CONFIG) -> FastAPI:
    """
    Add all routers to the FastAPI app
    """
    prefix = "/api"
    app.include_router(main_router, prefix=prefix)

    return app