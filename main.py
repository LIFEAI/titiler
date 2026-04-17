"""titiler instance for geo.place.fund — serves COG tiles from R2."""
import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from titiler.core.factory import TilerFactory
from titiler.core.errors import DEFAULT_STATUS_CODES, add_exception_handlers

app = FastAPI(
    title="geo-tiles",
    description="COG tile server for geo.place.fund",
    version="1.0.0",
)

# CORS — allow geo.place.fund and all *.dev.place.fund subdomains
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "https://geo.place.fund",
        "https://staged.geo.place.fund",
        "https://geo.dev.place.fund",
    ],
    allow_origin_regex=r"https://.*\.dev\.place\.fund",
    allow_credentials=True,
    allow_methods=["GET"],
    allow_headers=["*"],
)

cog = TilerFactory()
app.include_router(cog.router, prefix="/cog", tags=["Cloud Optimized GeoTIFF"])

add_exception_handlers(app, DEFAULT_STATUS_CODES)


@app.get("/health")
def health():
    return {"status": "ok", "service": "geo-tiles"}
