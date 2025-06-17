from __future__ import annotations
from typing import Any

import voluptuous as vol
from homeassistant import config_entries
from homeassistant.core import callback
from homeassistant.data_entry_flow import FlowResult

DOMAIN = "dhl_tracker"

CONF_API_KEY = "api_key"
CONF_TRACKINGS = "tracking_numbers"

DEFAULT_TRACKINGS = []

class DHLConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    """Handle a config flow for DHL Tracker."""

    VERSION = 1

    async def async_step_user(
        self, user_input: dict[str, Any] | None = None
    ) -> FlowResult:
        """Handle the initial step."""
        errors = {}

        if user_input is not None:
            # Validate API key format (basic validation)
            api_key = user_input[CONF_API_KEY].strip()
            if not api_key:
                errors[CONF_API_KEY] = "invalid_api_key"
            else:
                # Check if already configured
                await self.async_set_unique_id(f"dhl_tracker_{api_key[:8]}")
                self._abort_if_unique_id_configured()

                return self.async_create_entry(
                    title="DHL Tracker",
                    data={
                        CONF_API_KEY: api_key,
                    },
                    options={
                        CONF_TRACKINGS: DEFAULT_TRACKINGS
                    }
                )

        return self.async_show_form(
            step_id="user",
            data_schema=vol.Schema({
                vol.Required(CONF_API_KEY): str
            }),
            errors=errors,
            description_placeholders={
                "documentation_url": "https://developer.dhl.com/api-reference/dhl-paket-de-sendungsverfolgung-post-paket-deutschland"
            }
        )

    @staticmethod
    @callback
    def async_get_options_flow(
        config_entry: config_entries.ConfigEntry,
    ) -> DHLOptionsFlowHandler:
        """Create the options flow."""
        return DHLOptionsFlowHandler(config_entry)

class DHLOptionsFlowHandler(config_entries.OptionsFlow):
    """Handle DHL Tracker options."""

    def __init__(self, config_entry: config_entries.ConfigEntry) -> None:
        """Initialize options flow."""
        self.config_entry = config_entry
        self.tracking_numbers: list[dict[str, str]] = config_entry.options.get(CONF_TRACKINGS, [])

    async def async_step_init(
        self, user_input: dict[str, Any] | None = None
    ) -> FlowResult:
        """Manage the options."""
        return await self.async_step_add_tracking()

    async def async_step_add_tracking(
        self, user_input: dict[str, Any] | None = None
    ) -> FlowResult:
        """Add a new tracking number."""
        errors = {}

        if user_input is not None:
            carrier = user_input.get("carrier")
            tracking = user_input.get("tracking_number", "").strip()
            
            if not tracking:
                errors["tracking_number"] = "invalid_tracking_number"
            elif any(x.get("tracking_number") == tracking for x in self.tracking_numbers):
                errors["tracking_number"] = "tracking_already_exists"
            else:
                # Add new tracking number
                self.tracking_numbers.append({
                    "carrier": carrier,
                    "tracking_number": tracking
                })

                return self.async_create_entry(
                    title="",
                    data={CONF_TRACKINGS: self.tracking_numbers}
                )

        # Create current trackings display
        current_trackings = []
        for item in self.tracking_numbers:
            current_trackings.append(f"{item['carrier'].upper()}: {item['tracking_number']}")
        
        current_display = "\n".join(current_trackings) if current_trackings else "Keine Sendungen konfiguriert"

        schema = vol.Schema({
            vol.Required("carrier", default="dhl"): vol.In(["dhl", "hermes", "dpd"]),
            vol.Required("tracking_number"): str
        })

        return self.async_show_form(
            step_id="add_tracking",
            data_schema=schema,
            errors=errors,
            description_placeholders={
                "current_trackings": current_display
            }
        )
