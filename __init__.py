"""The salus component."""
import logging

from homeassistant import config_entries, core
from homeassistant.const import CONF_HOST, CONF_TOKEN
from homeassistant.helpers import device_registry as dr

from .config_flow import CONF_FLOW_TYPE, CONF_USER
from .const import DOMAIN

_LOGGER = logging.getLogger(__name__)

GATEWAY_PLATFORMS = ["climate", "binary_sensor"]


async def async_setup(hass: core.HomeAssistant, config: dict):
    """Set up the Salus component."""
    return True


async def async_setup_entry(
    hass: core.HomeAssistant, entry: config_entries.ConfigEntry
):
    """Set up the Salus components from a config entry."""
    hass.data[DOMAIN] = {}
    if entry.data[CONF_FLOW_TYPE] == CONF_USER:
        for component in GATEWAY_PLATFORMS:
            hass.async_create_task(
                hass.config_entries.async_forward_entry_setup(entry, component)
            )

        return True

    return True
