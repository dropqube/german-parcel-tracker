from abc import ABC, abstractmethod

class CarrierBase(ABC):
    @abstractmethod
    async def track(self, hass, tracking_number: str) -> dict:
        """Abfrage der Trackingdaten."""
        pass
