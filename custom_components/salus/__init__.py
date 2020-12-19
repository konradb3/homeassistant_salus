"""Support for Salus iT600."""
import logging

from homeassistant import config_entries, core

from .config_flow import CONF_FLOW_TYPE, CONF_USER
from .const import DOMAIN

_LOGGER = logging.getLogger(__name__)

GATEWAY_PLATFORMS = ["climate", "binary_sensor", "switch", "cover", "sensor"]


async def async_setup(hass: core.HomeAssistant, config: dict) -> bool:
    """Set up the Salus iT600 component."""
    return True


async def async_setup_entry(hass: core.HomeAssistant, entry: config_entries.ConfigEntry):
    """Set up components from a config entry."""
    hass.data[DOMAIN] = {}
    if entry.data[CONF_FLOW_TYPE] == CONF_USER:
        for component in GATEWAY_PLATFORMS:
            hass.async_create_task(
                hass.config_entries.async_forward_entry_setup(entry, component)
            )

        return True

    return True
