from dataclasses import asdict

from flask import Blueprint, jsonify

from services.shipment_service import get_all_shipments, get_shipment_by_id


shipment_blueprint = Blueprint("shipments", __name__, url_prefix="/api/shipments")


@shipment_blueprint.get("")
def get_all_shipments_endpoint():
    shipments = get_all_shipments()
    return jsonify([asdict(shipment) for shipment in shipments]), 200


@shipment_blueprint.get("/<shipment_id>")
def get_shipment_by_id_endpoint(shipment_id: str):
    shipment = get_shipment_by_id(shipment_id)

    if shipment is None:
        return jsonify({"error": "Shipment not found"}), 404

    return jsonify(asdict(shipment)), 200
