from __future__ import annotations

import logging
from datetime import timedelta

import voluptuous as vol

import homeassistant.helpers.config_validation as cv
from homeassistant.components.sensor import SensorDeviceClass, SensorEntity, SensorStateClass
from homeassistant.const import TEMP_CELSIUS
from homeassistant.core import HomeAssistant
from homeassistant.helpers.dispatcher import async_dispatcher_connect
from homeassistant.helpers.restore_state import RestoreEntity

from .const import DOMAIN, GLOBAL_PARALLEL_UPDATES
from .dcsyslib import *

_LOGGER = logging.getLogger(__name__)
PARALLEL_UPDATES = GLOBAL_PARALLEL_UPDATES
SCAN_INTERVAL = timedelta(seconds=60)
dcsys_sensors = []
hostname = ""


async def async_setup_platform(hass, config, async_add_entities, discovery_info=None):
    _LOGGER.info("DCSys sesnsor async_setup_platform gestart.")


async def async_setup_entry(hass, entry, async_add_devices):
    _LOGGER.info("DCSys sesnsor async_setup_entry gestart.")
    async_add_devices(dcsys_sensors)

def setHostname(h):
    global hostname
    hostname = h

class DcsysSensor(SensorEntity,RestoreEntity):
    def __init__(self, name, io_id, dc) -> None:
        _LOGGER.info("Init " + name)
        self._name = name

        # DCSys specifiek
        self._dcsys_io_id = io_id
        self._attr_state_class = SensorStateClass.MEASUREMENT
        self._attr_device_class = dc
        self._attr_native_value = None
        if dc == SensorDeviceClass.TEMPERATURE:
            self._attr_native_unit_of_measurement = TEMP_CELSIUS
        else:
            self._attr_native_unit_of_measurement = "raw"

        self._unique_id = (name + "_" + io_id).replace(" ", "_")

    async def async_update(self) -> None:
        _LOGGER.debug("async_update " + self._name)
        await self.hass.async_add_executor_job(self.doUpdate)

    def doUpdate(self) -> None:
        _LOGGER.debug("doUpdate " + self._name + " io:" + self._dcsys_io_id)
        global hostname
        self._attr_native_value = float(getIoCalculatedValue(hostname, self._dcsys_io_id))
        _LOGGER.debug("doUpdate " + self._name + " val:" + str(self._attr_native_value))

    async def async_added_to_hass(self) -> None:
        _LOGGER.debug("async_added_to_hass " + self._name)
        await super().async_added_to_hass()
        await self.hass.async_add_executor_job(self.doUpdate)

    @property
    def device_info(self):
        _LOGGER.debug("device_info " + self._unique_id)
        return {
            "identifiers": {(DOMAIN, "dcsys_sensors_device")},
            "name": "DCSys sensors device",
            "manufacturer": "Struyve",
            "model": "DCSys sensor",
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

