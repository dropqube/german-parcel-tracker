from .base import CarrierBase

class HermesCarrier(CarrierBase):
    async def track(self, hass, tracking_number: str) -> dict:
        return {
            "status": "unbekannt (Hermes nicht unterstützt)",
            "shipments": [
                {"status": {"status": "unbekannt", "description": "Kein offizieller Zugriff"},
                 "origin": {}, "destination": {}, "timestamp": None, "id": tracking_number}
            ]
        }
