import sys

relative_position = "../"
if relative_position not in sys.path:
    sys.path.insert(0, relative_position)

import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles

from src.config import CONFIG
from src.endpoints import include_all_routers
from src.handlers import MainHandler
from src.endpoints.router import router

# Integrating SQLite
from src.data import data_models
from src.data import SessionLocal, engine

data_models.Base.metadata.create_all(bind=engine)


class Application:
    @classmethod
    def setup(cls, app: FastAPI, handler: MainHandler, CONFIG):
        # Adding CORS middleware
        app.add_middleware(
            CORSMiddleware,
            allow_origins=[
                "http://localhost:5174"
            ],  # Chỉ chấp nhận yêu cầu từ frontend ở cổng 5174
            allow_credentials=True,
            allow_methods=["*"],
            allow_headers=["*"],
            expose_headers=["*"],
        )

        # Registering routers and exception handlers
        include_all_routers(app, handler, CONFIG)

        # Thêm router gốc
        app.include_router(router)

        # Thêm static file middleware
        app.mount("/static", StaticFiles(directory="static"), name="static")

        return app


app = FastAPI(
    title="Auto food order",
    description="Auto food prototype implementation",
)

app = Application.setup(app, MainHandler(), CONFIG)

# Running the app
if __name__ == "__main__":
    uvicorn.run("main:app", host="127.0.0.1", port=8080, reload=True, workers=8)
