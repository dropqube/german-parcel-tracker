import logging
from datetime import timedelta
from typing import Any

from homeassistant.components.sensor import SensorEntity, SensorDeviceClass
from homeassistant.helpers.update_coordinator import (
    DataUpdateCoordinator,
    UpdateFailed,
    CoordinatorEntity,
)
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.core import HomeAssistant, callback
from homeassistant.config_entries import ConfigEntry

from .carriers.dhl import DHLCarrier
from .carriers.hermes import HermesCarrier  
from .carriers.dpd import DPDCarrier

_LOGGER = logging.getLogger(__name__)

SCAN_INTERVAL = timedelta(minutes=30)
DOMAIN = "german-parcel-tracker"

async def async_setup_entry(
    hass: HomeAssistant, 
    entry: ConfigEntry, 
    async_add_entities: AddEntitiesCallback
) -> None:
    """Set up German Parcel Tracker sensors from config entry."""
    
    @callback
    def async_add_tracking_entities():
        """Add entities for tracking numbers."""
        api_key = entry.data.get("api_key")
        carrier_configs = entry.options.get("tracking_numbers", [])

        _LOGGER.info("Setting up German Parcel Tracker sensors - API Key: %s, Tracking configs: %s", 
                     "***" if api_key else "None", len(carrier_configs))

        if not carrier_configs:
            _LOGGER.info("No tracking numbers configured yet. Add some via Integration Options.")
            return

        new_entities = []
        for item in carrier_configs:
            carrier_type = item.get("carrier")
            tracking_number = item.get("tracking_number")

            _LOGGER.info("Processing tracking: %s - %s", carrier_type, tracking_number)

            if not carrier_type or not tracking_number:
                _LOGGER.warning("Skipping invalid tracking config: %s", item)
                continue

            # Check if entity already exists
            unique_id = f"track_{carrier_type}_{tracking_number}"
            if hass.states.get(f"sensor.{unique_id.lower()}"):
                _LOGGER.info("Entity %s already exists, skipping", unique_id)
                continue

            # Create carrier instance
            if carrier_type == "dhl":
                carrier = DHLCarrier(api_key)
            elif carrier_type == "hermes":
                carrier = HermesCarrier()
            elif carrier_type == "dpd":
                carrier = DPDCarrier()
            else:
                _LOGGER.warning("Unknown carrier type: %s", carrier_type)
                continue

            # Create coordinator
            coordinator = TrackingCoordinator(hass, carrier, tracking_number)
            
            # Create sensor entity
            sensor = TrackingSensor(coordinator, tracking_number, carrier_type)
            new_entities.append(sensor)
            _LOGGER.info("Created sensor: %s", sensor.unique_id)

        if new_entities:
            _LOGGER.info("Adding %d new entities to Home Assistant", len(new_entities))
            async_add_entities(new_entities, True)
            
            # Start coordinators after entities are added
            for entity in new_entities:
                hass.async_create_task(entity.coordinator.async_config_entry_first_refresh())

    # Initial setup
    async_add_tracking_entities()
    
    # Listen for options updates
    @callback
    def async_options_updated(hass: HomeAssistant, entry: ConfigEntry):
        """Handle options update."""
        _LOGGER.info("Options updated, adding new tracking entities")
        async_add_tracking_entities()
    
    # Register the update listener
    entry.async_on_unload(
        entry.add_update_listener(async_options_updated)
    )

class TrackingCoordinator(DataUpdateCoordinator):
    """Coordinator to manage tracking data updates."""

    def __init__(self, hass: HomeAssistant, carrier, tracking_number: str) -> None:
        """Initialize the coordinator."""
        super().__init__(
            hass,
            _LOGGER,
            name=f"Tracking Data {tracking_number}",
            update_interval=SCAN_INTERVAL,
        )
        self.carrier = carrier
        self.tracking_number = tracking_number

    async def _async_update_data(self) -> dict[str, Any]:
        """Update tracking data."""
        try:
            _LOGGER.info("Updating tracking data for %s", self.tracking_number)
            data = await self.carrier.track(self.hass, self.tracking_number)
            _LOGGER.info("Got tracking data for %s: %s", self.tracking_number, data)
            return data
        except Exception as err:
            _LOGGER.error("Error fetching tracking data for %s: %s", self.tracking_number, err)
            raise UpdateFailed(f"Error fetching tracking data for {self.tracking_number}: {err}") from err

class TrackingSensor(CoordinatorEntity, SensorEntity):
    """Sensor for tracking package status."""

    def __init__(
        self, 
        coordinator: TrackingCoordinator, 
        tracking_number: str, 
        carrier: str
    ) -> None:
        """Initialize the sensor."""
        super().__init__(coordinator)
        self._tracking_number = tracking_number
        self._carrier = carrier
        self._attr_unique_id = f"track_{self._carrier}_{self._tracking_number}"
        self._attr_name = f"{self._carrier.upper()} Package {self._tracking_number}"
        self._attr_device_class = SensorDeviceClass.ENUM
        
        _LOGGER.info("Initialized sensor: %s (unique_id: %s)", self._attr_name, self._attr_unique_id)

    @property
    def native_value(self) -> str:
        """Return the state of the sensor."""
        if not self.coordinator.data:
            return "unknown"
        
        try:
            status = self.coordinator.data["shipments"][0]["status"]["status"]
            _LOGGER.debug("Sensor %s status: %s", self._attr_unique_id, status)
            return status
        except (KeyError, IndexError, TypeError) as err:
            _LOGGER.warning("Error getting status for %s: %s", self._attr_unique_id, err)
            return "unknown"

    @property
    def extra_state_attributes(self) -> dict[str, Any]:
        """Return additional state attributes."""
        if not self.coordinator.data:
            return {
                "tracking_number": self._tracking_number,
                "carrier": self._carrier,
            }
        
        try:
            shipment = self.coordinator.data["shipments"][0]
            return {
                "tracking_number": shipment.get("id", self._tracking_number),
                "origin": shipment.get("origin", {}).get("address", {}).get("addressLocality"),
                "destination": shipment.get("destination", {}).get("address", {}).get("addressLocality"),
                "status_description": shipment.get("status", {}).get("description"),
                "timestamp": shipment.get("status", {}).get("timestamp"),
                "carrier": self._carrier,
                "last_update": getattr(self.coordinator, "last_update_success_time", None),
            }
        except (KeyError, TypeError) as err:
            _LOGGER.warning("Error getting attributes for %s: %s", self._attr_unique_id, err)
            return {
                "tracking_number": self._tracking_number,
                "carrier": self._carrier,
                "last_update": getattr(self.coordinator, "last_update_success_time", None),
                "error": str(err),
            }

    @property
    def icon(self) -> str:
        """Return the icon for this sensor."""
        status = self.native_value
        if status in ["delivered", "zugestellt"]:
            return "mdi:package-check"
        elif status in ["in_transit", "unterwegs"]:
            return "mdi:truck-delivery"
        elif status in ["unknown", "unbekannt"]:
            return "mdi:package-variant"
        else:
            return "mdi:package"

    @property
    def available(self) -> bool:
        """Return if entity is available."""
        return self.coordinator.last_update_success or self.coordinator.data is not None
