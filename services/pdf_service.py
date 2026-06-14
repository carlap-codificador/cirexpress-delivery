from pathlib import Path

from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.platypus import Image, Paragraph, SimpleDocTemplate, Spacer, Table

from models.pod_model import ProofOfDelivery
from models.shipment_model import Shipment


BASE_DIR = Path(__file__).resolve().parent.parent
OUTPUTS_DIR = BASE_DIR / "outputs"


def generate_pod_pdf(shipment: Shipment, pod: ProofOfDelivery) -> str:
    OUTPUTS_DIR.mkdir(exist_ok=True)

    pdf_path = OUTPUTS_DIR / f"pod_{pod.pod_id}.pdf"
    document = SimpleDocTemplate(str(pdf_path), pagesize=letter)
    styles = getSampleStyleSheet()

    content = [
        Paragraph("CIRExpress Proof of Delivery", styles["Title"]),
        Spacer(1, 16),
        Paragraph("Shipment Information", styles["Heading2"]),
        _build_shipment_table(shipment),
        Spacer(1, 16),
        Paragraph("Delivery Confirmation", styles["Heading2"]),
        _build_pod_table(pod),
        Spacer(1, 12),
        Paragraph("Receiver Signature", styles["Heading3"]),
        Image(pod.signature_path, width=240, height=90),
    ]

    document.build(content)
    return str(pdf_path)


def _build_shipment_table(shipment: Shipment) -> Table:
    return Table(
        [
            ["Shipment ID", shipment.shipment_id],
            ["Consol Number", shipment.consol_number],
            ["Date", shipment.date],
            ["Consignor", shipment.consignor],
            ["Consignee", shipment.consignee],
            ["Notify Party", shipment.notify_party],
            ["Delivery Address", shipment.delivery_address],
            ["Carrier", shipment.carrier],
            ["Vessel", shipment.vessel],
            ["Bill of Lading", shipment.bill_of_lading],
            ["Release Type", shipment.release_type],
            ["Origin", shipment.origin],
            ["Destination", shipment.destination],
            ["Port of Loading", shipment.port_of_loading],
            ["Port of Discharge", shipment.port_of_discharge],
            ["ETA", shipment.eta],
            ["ETD", shipment.etd],
            ["Marks and Numbers", shipment.marks_numbers],
            ["Goods Description", shipment.goods_description],
            ["Gross Weight", shipment.gross_weight],
            ["Volume", shipment.volume],
            ["Packs", shipment.packs],
            ["Trucker Name", shipment.trucker_name],
        ],
        colWidths=[140, 360],
    )


def _build_pod_table(pod: ProofOfDelivery) -> Table:
    return Table(
        [
            ["POD ID", pod.pod_id],
            ["Shipment ID", pod.shipment_id],
            ["Receiver Name", pod.receiver_name],
            ["Signature Path", pod.signature_path],
            ["Delivered At", pod.delivered_at],
            ["Photo Path", pod.photo_path or ""],
            ["GPS Location", pod.gps_location or ""],
            ["PDF Path", pod.pdf_path or ""],
        ],
        colWidths=[140, 360],
    )
