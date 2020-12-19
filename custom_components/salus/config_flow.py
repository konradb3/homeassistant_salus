"""Config flow to configure Salus iT600 component."""
import logging

import voluptuous as vol

from homeassistant import config_entries
from homeassistant.const import CONF_HOST, CONF_NAME, CONF_TOKEN

from pyit600.exceptions import IT600AuthenticationError, IT600ConnectionError
from pyit600.gateway import IT600Gateway

# pylint: disable=unused-import
from .const import DOMAIN

_LOGGER = logging.getLogger(__name__)

CONF_FLOW_TYPE = "config_flow_device"
CONF_USER = "user"
DEFAULT_GATEWAY_NAME = "Salus iT600 Gateway"

GATEWAY_SETTINGS = {
    vol.Required(CONF_HOST): str,
    vol.Required(CONF_TOKEN): vol.All(str, vol.Length(min=16, max=16)),
    vol.Optional(CONF_NAME, default=DEFAULT_GATEWAY_NAME): str,
}


class SalusFlowHandler(config_entries.ConfigFlow, domain=DOMAIN):
    """Handle a Salus config flow."""

    VERSION = 1
    CONNECTION_CLASS = config_entries.CONN_CLASS_LOCAL_POLL

    async def async_step_user(self, user_input=None):
        """Handle a flow initialized by the user to configure a gateway."""
        errors = {}
        if user_input is not None:
            token = user_input[CONF_TOKEN]
            host = user_input[CONF_HOST]

            # Try to connect to a Salus Gateway.
            gateway = IT600Gateway(host=host, euid=token)
            try:
                unique_id = await gateway.connect()
                await self.async_set_unique_id(unique_id)
                self._abort_if_unique_id_configured()
                return self.async_create_entry(
                    title=user_input[CONF_NAME],
                    data={
                        CONF_FLOW_TYPE: CONF_USER,
                        CONF_HOST: host,
                        CONF_TOKEN: token,
                        "mac": unique_id,
                    },
                )
            except IT600ConnectionError:
                errors["base"] = "connect_error"
            except IT600AuthenticationError:
                errors["base"] = "auth_error"

        schema = vol.Schema(GATEWAY_SETTINGS)

        return self.async_show_form(step_id="user", data_schema=schema, errors=errors)
