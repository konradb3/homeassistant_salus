"""Support for cover (roller shutter) devices."""
from datetime import timedelta
import logging
import async_timeout

import voluptuous as vol
from homeassistant.components.cover import PLATFORM_SCHEMA, ATTR_POSITION, CoverEntity

from homeassistant.const import (
    CONF_HOST,
    CONF_TOKEN
)

import homeassistant.helpers.config_validation as cv
from homeassistant.helpers.update_coordinator import DataUpdateCoordinator, UpdateFailed

from .const import DOMAIN

_LOGGER = logging.getLogger(__name__)

PLATFORM_SCHEMA = PLATFORM_SCHEMA.extend(
    {
        vol.Required(CONF_HOST): cv.string,
        vol.Required(CONF_TOKEN): cv.string,
    }
)


async def async_setup_entry(hass, config_entry, async_add_entities):
    """Set up Salus cover devices from a config entry."""

    gateway = hass.data[DOMAIN][config_entry.entry_id]

    async def async_update_data():
        """Fetch data from API endpoint.

        This is the place to pre-process the data to lookup tables
        so entities can quickly look up their data.
        """
        async with async_timeout.timeout(10):
            await gateway.poll_status()
            return gateway.get_cover_devices()

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

    async_add_entities(SalusCover(coordinator, idx, gateway) for idx
                       in coordinator.data)


async def async_setup_platform(hass, config, async_add_entities, discovery_info=None):
    """Set up the cover platform."""
    pass


class SalusCover(CoverEntity):
    """Representation of a binary sensor."""

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

    @property
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
    def name(self):
        """Return the name of the sensor."""
        return self._coordinator.data.get(self._idx).name

    @property
    def supported_features(self):
        """Return the list of supported features."""
        return self._coordinator.data.get(self._idx).supported_features

    @property
    def device_class(self):
        """Return the device class of the sensor."""
        return self._coordinator.data.get(self._idx).device_class

    @property
    def current_cover_position(self):
        """Return the current position of the cover."""
        return self._coordinator.data.get(self._idx).current_cover_position

    @property
    def is_opening(self):
        """Return if the cover is opening or not."""
        return self._coordinator.data.get(self._idx).is_opening

    @property
    def is_closing(self):
        """Return if the cover is closing or not."""
        return self._coordinator.data.get(self._idx).is_closing

    @property
    def is_closed(self):
        """Return if the cover is closed."""
        return self._coordinator.data.get(self._idx).is_closed

    async def async_open_cover(self, **kwargs):
        """Open the cover."""
        await self._gateway.open_cover(self._idx)
        await self._coordinator.async_request_refresh()

    async def async_close_cover(self, **kwargs):
        """Close the cover."""
        await self._gateway.close_cover(self._idx)
        await self._coordinator.async_request_refresh()

    async def async_set_cover_position(self, **kwargs):
        """Move the cover to a specific position."""
        position = kwargs.get(ATTR_POSITION)
        if position is None:
            return
        await self._gateway.set_cover_position(self._idx, position)
        await self._coordinator.async_request_refresh()
