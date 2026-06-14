from dataclasses import dataclass


@dataclass
class Shipment:
    shipment_id: str
    consol_number: str
    date: str
    consignor: str
    consignee: str
    notify_party: str
    delivery_address: str
    carrier: str
    vessel: str
    bill_of_lading: str
    release_type: str
    origin: str
    destination: str
    port_of_loading: str
    port_of_discharge: str
    eta: str
    etd: str
    marks_numbers: str
    goods_description: str
    gross_weight: str
    volume: str
    packs: str
    trucker_name: str
