"""Support for switch (smart plug/relay/roller shutter) devices."""
from datetime import timedelta
import logging
import async_timeout

import voluptuous as vol
from homeassistant.components.switch import PLATFORM_SCHEMA, SwitchEntity

from homeassistant.const import (
    CONF_HOST,
    CONF_TOKEN
)

import homeassistant.helpers.config_validation as cv
from homeassistant.helpers.update_coordinator import DataUpdateCoordinator, UpdateFailed

from pyit600.exceptions import IT600AuthenticationError, IT600ConnectionError
from pyit600.gateway import IT600Gateway

_LOGGER = logging.getLogger(__name__)

PLATFORM_SCHEMA = PLATFORM_SCHEMA.extend(
    {
        vol.Required(CONF_HOST): cv.string,
        vol.Required(CONF_TOKEN): cv.string,
    }
)


async def async_setup_entry(hass, config_entry, async_add_entities):
    """Set up Salus switches from a config entry."""
    await async_setup_platform(hass, config_entry.data, async_add_entities)


async def async_setup_platform(hass, config, async_add_entities, discovery_info=None):
    """Set up the switch platform."""

    gateway = IT600Gateway(host=config[CONF_HOST], euid=config[CONF_TOKEN])
    try:
        await gateway.connect()
    except IT600ConnectionError as ce:
        _LOGGER.error("Connection error: check if you have specified gateway's HOST correctly.")
        return False
    except IT600AuthenticationError as ae:
        _LOGGER.error("Authentication error: check if you have specified gateway's TOKEN correctly.")
        return False

    async def async_update_data():
        """Fetch data from API endpoint.

        This is the place to pre-process the data to lookup tables
        so entities can quickly look up their data.
        """
        async with async_timeout.timeout(10):
            await gateway.poll_status()
            return gateway.get_switch_devices()

    coordinator = DataUpdateCoordinator(
        hass,
        _LOGGER,
        # Name of the data. For logging purposes.
        name="sensor",
        update_method=async_update_data,
        # Polling interval. Will only be polled if there are subscribers.
        update_interval=timedelta(seconds=30),
    )

    # Fetch initial data so we have data when entities subscribe
    await coordinator.async_refresh()

    async_add_entities(SalusSwitch(coordinator, idx, gateway) for idx
                       in coordinator.data)


class SalusSwitch(SwitchEntity):
    """Representation of a switch."""

    def __init__(self, coordinator, idx, gateway):
        """Initialize the sensor."""
        self._coordinator = coordinator
        self._idx = idx
        self._gateway = gateway

    async def async_update(self):
        """Update the entity.
        Only used by the generic entity update service.
        """
        await self._coordinator.async_request_refresh()

    async def async_added_to_hass(self):
        """When entity is added to hass."""
        self.async_on_remove(
            self._coordinator.async_add_listener(self.async_write_ha_state)
        )

    def available(self):
        """Return if entity is available."""
        return self._coordinator.data.get(self._idx).available

    @property
    def device_info(self):
        """Return the device info."""
        return {
            "name": self._coordinator.data.get(self._idx).name,
            "identifiers": {("salus", self._coordinator.data.get(self._idx).unique_id)},
            "manufacturer": self._coordinator.data.get(self._idx).manufacturer,
            "model": self._coordinator.data.get(self._idx).model,
            "sw_version": self._coordinator.data.get(self._idx).sw_version
        }

    @property
    def unique_id(self):
        """Return the unique id."""
        return self._coordinator.data.get(self._idx).unique_id

    @property
    def should_poll(self):
        """No need to poll. Coordinator notifies entity of updates."""
        return False

    @property
    def device_class(self):
        """Return the device class of the sensor."""
        return self._coordinator.data.get(self._idx).device_class

    @property
    def is_on(self):
        """Return true if it is on."""
        return self._coordinator.data.get(self._idx).is_on

    async def async_turn_on(self, **kwargs):
        """Turn the switch on."""
        await self._gateway.turn_on_switch_device(self._idx)
        await self._coordinator.async_request_refresh()

    async def async_turn_off(self, **kwargs):
        """Turn the switch off."""
        await self._gateway.turn_off_switch_device(self._idx)
        await self._coordinator.async_request_refresh()
