from __future__ import annotations

import logging
from datetime import timedelta

import voluptuous as vol

# Import the device class from the component that you want to support
import homeassistant.helpers.config_validation as cv
from homeassistant.components.switch import SwitchDeviceClass, SwitchEntity
from homeassistant.core import HomeAssistant

from .const import DOMAIN, GLOBAL_PARALLEL_UPDATES
from .dcsyslib import *

_LOGGER = logging.getLogger(__name__)
PARALLEL_UPDATES = GLOBAL_PARALLEL_UPDATES
SCAN_INTERVAL = timedelta(seconds=10)
dcsys_schakelaars = []
hostname = ""


async def async_setup_platform(hass, config, async_add_entities, discovery_info=None):
    _LOGGER.info("DCSys sesnsor async_setup_platform gestart.")

async def async_setup_entry(hass, entry, async_add_devices):
    _LOGGER.info("DCSys sesnsor async_setup_entry gestart.")
    async_add_devices(dcsys_schakelaars)

def setHostname(h):
    global hostname
    hostname = h

class DcsysSchakelaar(SwitchEntity):
    def __init__(self, name, io_id) -> None:
        _LOGGER.info("Init " + name)
        self._name = name

        # DCSys specifiek
        self._dcsys_io_id = io_id
        self._attr_device_class = SwitchDeviceClass.SWITCH
        self._attr_native_value = 0
        self._attr_state = 0
        self._unique_id = (name + "_" + io_id).replace(" ", "_")

    async def async_update(self) -> None:
        _LOGGER.debug("async_update " + self._name)
        await self.hass.async_add_executor_job(self.doUpdate)

    def doUpdate(self) -> None:
        _LOGGER.debug("doUpdate " + self._name + " io:" + self._dcsys_io_id)
        global hostname
        self._attr_state = int(getIoRawValue(hostname, self._dcsys_io_id))
        if self._attr_state == 0:
            self._state = False
        else:
            self._state = True

    def doActon(self) -> None:
        _LOGGER.debug("doActon " + self._name)
        global hostname
        if self._state:
            setIoRawValue(hostname,self._dcsys_io_id,1)
        else:
            setIoRawValue(hostname,self._dcsys_io_id,0)

    async def async_turn_on(self, **kwargs):
        _LOGGER.debug("async_turn_on " + self._name)
        self._state = True
        await self.hass.async_add_executor_job(self.doActon)
            
        self.async_schedule_update_ha_state(True)

    async def async_turn_off(self, **kwargs):
        _LOGGER.debug("async_turn_off " + self._name)
        self._state = False
        await self.hass.async_add_executor_job(self.doActon)
        self.async_schedule_update_ha_state(True)

    @property
    def device_info(self):
        _LOGGER.info("device_info " + self._unique_id)
        return {
            "identifiers": {(DOMAIN, "dcsys_schakelaars_device")},
            "name": "DCSys schakelaars device",
            "manufacturer": "Struyve",
            "model": "DCSys schakelaar",
            "sw_version": "0.1",
        }

    @property
    def name(self) -> str:
        return self._name

    @property
    def should_poll(self):
        return True

    @property
    def unique_id(self) -> str:
        return self._unique_id

    @property
    def is_on(self) -> bool | None:
        _LOGGER.debug("is_on " + self._name)
        return self._attr_state
