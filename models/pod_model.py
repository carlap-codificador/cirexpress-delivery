from dataclasses import dataclass
from typing import Optional


@dataclass
class ProofOfDelivery:
    pod_id: str
    shipment_id: str
    receiver_name: str
    signature_path: str
    delivered_at: str
    photo_path: Optional[str]
    gps_location: Optional[str]
    pdf_path: Optional[str]
