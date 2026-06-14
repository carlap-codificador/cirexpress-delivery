import json
from pathlib import Path
from typing import Optional

from models.shipment_model import Shipment


BASE_DIR = Path(__file__).resolve().parent.parent
SHIPMENTS_FILE = BASE_DIR / "data" / "shipments.json"


def load_shipments() -> list[Shipment]:
    with open(SHIPMENTS_FILE, "r", encoding="utf-8") as file:
        data = json.load(file)

    return [Shipment(**item) for item in data]


def get_all_shipments() -> list[Shipment]:
    return load_shipments()


def get_shipment_by_id(shipment_id: str) -> Optional[Shipment]:
    shipments = load_shipments()

    for shipment in shipments:
        if shipment.shipment_id == shipment_id:
            return shipment

    return None
