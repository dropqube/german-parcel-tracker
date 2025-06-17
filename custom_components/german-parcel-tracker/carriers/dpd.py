from .base import CarrierBase

class DPDCarrier(CarrierBase):
    async def track(self, hass, tracking_number: str) -> dict:
        return {
            "status": "unbekannt (DPD nicht integriert)",
            "shipments": [
                {"status": {"status": "unbekannt", "description": "Nur mit API-Key über DPD-Partner"},
                 "origin": {}, "destination": {}, "timestamp": None, "id": tracking_number}
            ]
        }
