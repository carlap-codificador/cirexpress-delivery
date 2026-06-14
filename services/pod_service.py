import base64
import binascii
import json
from dataclasses import asdict
from datetime import datetime
from pathlib import Path
from typing import Optional
from uuid import uuid4

from models.pod_model import ProofOfDelivery


BASE_DIR = Path(__file__).resolve().parent.parent
PODS_FILE = BASE_DIR / "data" / "pods.json"
OUTPUTS_DIR = BASE_DIR / "outputs"


def validate_delivery_data(receiver_name: str, signature: str) -> None:
    if not receiver_name:
        raise ValueError("receiver_name is required")

    if not signature:
        raise ValueError("signature is required")


def register_delivery(
    shipment_id: str,
    receiver_name: str,
    signature: str,
    photo_path: Optional[str] = None,
    gps_location: Optional[str] = None,
    pdf_path: Optional[str] = None,
) -> ProofOfDelivery:
    validate_delivery_data(receiver_name, signature)
    signature_path = save_signature_image(signature)

    pod = ProofOfDelivery(
        pod_id=str(uuid4()),
        shipment_id=shipment_id,
        receiver_name=receiver_name,
        signature_path=signature_path,
        delivered_at=datetime.utcnow().isoformat(),
        photo_path=photo_path,
        gps_location=gps_location,
        pdf_path=pdf_path,
    )

    save_pod(pod)
    return pod


def save_signature_image(signature: str) -> str:
    OUTPUTS_DIR.mkdir(exist_ok=True)

    if "," in signature:
        signature = signature.split(",", 1)[1]

    try:
        signature_bytes = base64.b64decode(signature, validate=True)
    except (binascii.Error, ValueError) as error:
        raise ValueError("signature must be a valid base64 image") from error

    signature_path = OUTPUTS_DIR / f"signature_{uuid4()}.png"

    with open(signature_path, "wb") as file:
        file.write(signature_bytes)

    return str(signature_path)


def save_pod(pod: ProofOfDelivery) -> None:
    pods = load_pods()
    pods.append(asdict(pod))

    with open(PODS_FILE, "w", encoding="utf-8") as file:
        json.dump(pods, file, indent=2)


def update_pod_pdf_path(pod_id: str, pdf_path: str) -> None:
    pods = load_pods()

    for pod in pods:
        if pod["pod_id"] == pod_id:
            pod["pdf_path"] = pdf_path
            break

    with open(PODS_FILE, "w", encoding="utf-8") as file:
        json.dump(pods, file, indent=2)


def load_pods() -> list[dict]:
    with open(PODS_FILE, "r", encoding="utf-8") as file:
        return json.load(file)
