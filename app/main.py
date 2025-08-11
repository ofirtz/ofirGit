from datetime import date
from pathlib import Path
from typing import List, Optional

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles

from .models import SearchRequest, SearchResult, Hotel
from .utils import load_hotels_dataset, compute_nights, find_cheapest_hotel

BASE_DIR = Path(__file__).resolve().parent
DATA_FILE = BASE_DIR / "data" / "hotels.json"
STATIC_DIR = BASE_DIR / "static"

app = FastAPI(title="Hotel Finder API", description="API למציאת המלון הזול ביותר לזוג לפי יעד ותאריכים", version="1.0.0")

# אם בעתיד הממשק ישרת מדומיין אחר, CORS כבר מוכן
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# שרת קבצים סטטיים
app.mount("/static", StaticFiles(directory=STATIC_DIR), name="static")


@app.get("/", include_in_schema=False)
async def serve_index() -> FileResponse:
    index_file = STATIC_DIR / "index.html"
    return FileResponse(index_file)


@app.post("/api/search", response_model=SearchResult)
async def search_hotels(request: SearchRequest) -> SearchResult:
    hotels: List[Hotel] = load_hotels_dataset(DATA_FILE)

    nights = compute_nights(request.check_in, request.check_out)
    if nights < 1:
        raise HTTPException(status_code=400, detail="תאריכים לא תקינים: חייב להיות לפחות לילה אחד, ותאריך היציאה אחרי תאריך הכניסה")

    cheapest = find_cheapest_hotel(hotels, destination=request.destination)
    if cheapest is None:
        raise HTTPException(status_code=404, detail="יעד לא נמצא במאגר המלונות")

    total_price = nights * cheapest.price_per_night_for_two

    return SearchResult(
        hotel_name=cheapest.name,
        city=cheapest.city,
        region=cheapest.region,
        price_per_night=cheapest.price_per_night_for_two,
        nights=nights,
        total_price=total_price,
    )