import logging

import homeassistant.helpers.config_validation as cv
import voluptuous as vol
from homeassistant import config_entries
from homeassistant.const import CONF_HOST

from .const import DOMAIN

_LOGGER = logging.getLogger(__name__)

class DcsysConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):

    def __init__(self):
        _LOGGER.info("Flow __init__")
        self._hostname = vol.UNDEFINED

    async def async_step_user(self, user_input=None):
        _LOGGER.info("Flow async_step_user")
        errors = {}

        if self._async_current_entries():
            return self.async_abort(reason="already_configured")

        if user_input is not None:
            self._hostname = user_input[CONF_HOST]

            return self.async_create_entry(
                title=user_input[CONF_HOST],
                data=user_input,
            )

        return self.async_show_form(
            step_id="user",
            data_schema=vol.Schema( { vol.Required(CONF_HOST, default="dcsys.struyve.local"): str, } ),
            errors=errors,
        )

    async def async_step_import(self, user_input):
        _LOGGER.info("Flow async_step_import")
        
        if self._async_current_entries():
            return self.async_abort(reason="already_configured")

        hostname = user_input[CONF_HOST]
        return self.async_create_entry(
            title=f"{hostname} (from configuration)",
            data={
                CONF_HOST: hostname,
            },
        )