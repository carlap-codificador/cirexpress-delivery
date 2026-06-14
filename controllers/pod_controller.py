from dataclasses import asdict

from flask import Blueprint, jsonify, request

from services.pdf_service import generate_pod_pdf
from services.pod_service import register_delivery, update_pod_pdf_path
from services.shipment_service import get_shipment_by_id


pod_blueprint = Blueprint("pods", __name__, url_prefix="/api/shipments")


@pod_blueprint.post("/<shipment_id>/pod")
def register_delivery_endpoint(shipment_id: str):
    shipment = get_shipment_by_id(shipment_id)

    if shipment is None:
        return jsonify({"error": "Shipment not found"}), 404

    request_data = request.get_json(silent=True) or {}

    try:
        pod = register_delivery(
            shipment_id=shipment_id,
            receiver_name=request_data.get("receiver_name"),
            signature=request_data.get("signature"),
            photo_path=request_data.get("photo_path"),
            gps_location=request_data.get("gps_location"),
        )

        pdf_path = generate_pod_pdf(shipment, pod)
        pod.pdf_path = pdf_path
        update_pod_pdf_path(pod.pod_id, pdf_path)

        return jsonify(
            {
                "message": "Delivery registered successfully",
                "pod": asdict(pod),
            }
        ), 201
    except ValueError as error:
        return jsonify({"error": str(error)}), 400
