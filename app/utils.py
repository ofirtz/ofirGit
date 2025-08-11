from __future__ import annotations
from datetime import date
from pathlib import Path
from typing import Iterable, List, Optional
import json

from .models import Hotel


def load_hotels_dataset(json_path: Path) -> List[Hotel]:
    with open(json_path, "r", encoding="utf-8") as f:
        raw = json.load(f)
    return [Hotel(**item) for item in raw]


def compute_nights(check_in: date, check_out: date) -> int:
    return (check_out - check_in).days


def normalize_text(value: str) -> str:
    return value.strip().lower()


def destination_matches(hotel: Hotel, destination: str) -> bool:
    d = normalize_text(destination)
    return d in normalize_text(hotel.city) or d in normalize_text(hotel.region)


def find_cheapest_hotel(hotels: Iterable[Hotel], destination: str) -> Optional[Hotel]:
    candidates: List[Hotel] = [h for h in hotels if destination_matches(h, destination)]
    if not candidates:
        return None
    return min(candidates, key=lambda h: h.price_per_night_for_two)