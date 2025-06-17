import asyncio
import aiohttp
import logging
from typing import Any

from .base import CarrierBase

_LOGGER = logging.getLogger(__name__)

class DHLCarrier(CarrierBase):
    """DHL Carrier implementation using official API."""
    
    # During the testing phase we use the sandbox endpoint of the
    # DHL Paket DE Sendungsverfolgung API. For production this
    # should be changed to "https://api-eu.dhl.com/parcel/de/tracking/v0/shipments".
    API_URL = "https://api-sandbox.dhl.com/parcel/de/tracking/v0/shipments"
    # API_URL = "https://api-eu.dhl.com/track/shipments"


    def __init__(self, api_key: str) -> None:
        """Initialize DHL carrier with API key."""
        self.api_key = api_key

    async def track(self, hass, tracking_number: str) -> dict[str, Any]:
        """Track a DHL shipment."""
        headers = {
            "DHL-API-Key": self.api_key,
            "Accept": "application/json"
        }
        params = {"trackingNumber": tracking_number}

        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(
                    self.API_URL, 
                    headers=headers, 
                    params=params,
                    timeout=aiohttp.ClientTimeout(total=30)
                ) as response:
                    if response.status == 200:
                        data = await response.json()
                        return data
                    elif response.status == 404:
                        # Tracking number not found
                        return {
                            "shipments": [{
                                "id": tracking_number,
                                "status": {
                                    "status": "not_found",
                                    "description": "Sendungsnummer nicht gefunden"
                                },
                                "origin": {},
                                "destination": {},
                                "timestamp": None
                            }]
                        }
                    else:
                        response.raise_for_status()
                        
        except aiohttp.ClientError as err:
            _LOGGER.error("Error fetching DHL tracking data for %s: %s", tracking_number, err)
            return {
                "shipments": [{
                    "id": tracking_number,
                    "status": {
                        "status": "error",
                        "description": f"Fehler beim Abrufen: {err}"
                    },
                    "origin": {},
                    "destination": {},
                    "timestamp": None
                }]
            }
        except Exception as err:
            _LOGGER.error("Unexpected error for DHL tracking %s: %s", tracking_number, err)
            return {
                "shipments": [{
                    "id": tracking_number,
                    "status": {
                        "status": "unknown",
                        "description": f"Unerwarteter Fehler: {err}"
                    },
                    "origin": {},
                    "destination": {},
                    "timestamp": None
                }]
            }
