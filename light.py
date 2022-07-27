"""Platform for light integration."""
from __future__ import annotations

import logging
from datetime import timedelta

import voluptuous as vol

# Import the device class from the component that you want to support
import homeassistant.helpers.config_validation as cv
from homeassistant.components.light import (ATTR_BRIGHTNESS, SUPPORT_BRIGHTNESS, PLATFORM_SCHEMA, LightEntity)
from homeassistant.core import HomeAssistant

from .const import DOMAIN, GLOBAL_PARALLEL_UPDATES
from .dcsyslib import *

_LOGGER = logging.getLogger(__name__)
PARALLEL_UPDATES = GLOBAL_PARALLEL_UPDATES
SCAN_INTERVAL = timedelta(seconds=10)
dcsys_lichten = []
hostname = ""

async def async_setup_platform(hass, config, async_add_entities, discovery_info=None):
    _LOGGER.info("DCSys licht async_setup_platform gestart.")

async def async_setup_entry(hass, entry, async_add_devices):
    _LOGGER.info("DCSys light async_setup_entry gestart.")
    async_add_devices(dcsys_lichten)

def setHostname(h):
    global hostname
    hostname = h
    
class DcsysLicht(LightEntity):

    def __init__(self,name,io_id,status,min,max,step) -> None:
        _LOGGER.info("Init " + name)
        self._name = name

        # DCSys specifiek
        self._dcsys_io_id = io_id
        self._dcsys_seq_reverse = 0
        self._dcsys_seq_set = 0
        self._dcsys_seq_on = 0
        self._dcsys_seq_off = 0
        self._dcsys_raw_value = 0.0
        self._dcsys_min = min
        self._dcsys_max = max
        self._dcsys_ratio = (self._dcsys_max - self._dcsys_min)/255
        

        self._state = status
        self._brightness = self.convertRawToBrightness(self._dcsys_raw_value)
        self._unique_id = ( name+ "_" + io_id).replace(" ", "_")
        
        #self.doUpdate()
        #self.async_schedule_update_ha_state(True)

    def convertRawToBrightness(self,raw) -> int:
        retval = int (round( (raw - self._dcsys_min)/self._dcsys_ratio,0))
        if retval < 0:
            retval = 0

        _LOGGER.debug("convertRawToBrightness " + self._name + " ratio:" + str(self._dcsys_ratio) + " raw:" + " br:" + str(retval))
        return retval

    def convertBrightnessToRaw(self,br) -> int:
        retval = int (round( (br*self._dcsys_ratio)+self._dcsys_min ,0) )
        _LOGGER.debug("convertRawToBrightness " + self._name + " ratio:" + str(self._dcsys_ratio) + " br:" + " raw:" + str(retval))
        return retval

    async def async_update(self) -> None:
        _LOGGER.debug("async_update " + self._name)
        await self.hass.async_add_executor_job(self.doUpdate)
    
    def doActon(self) -> None:
        _LOGGER.debug("doActon " + self._name + " br:" + str(self._brightness)+ " io:" + self._dcsys_io_id)
        global hostname
        ovalue = 0
        if (self._state and self._dcsys_max > 1):
            ovalue = self.convertBrightnessToRaw(self._brightness)
        elif (self._state ):
            ovalue = 1
        
        setIoRawValue(hostname,self._dcsys_io_id,ovalue)

    def doUpdate(self) -> None:
        _LOGGER.debug("doUpdate " + self._name + " br:" + str(self._brightness)+ " io:" + self._dcsys_io_id)
        global hostname
        self._dcsys_raw_value = float(getIoRawValue(hostname,self._dcsys_io_id))
        if self._dcsys_raw_value > 0.0:
            self._state = True
            self._brightness = self.convertRawToBrightness(self._dcsys_raw_value)
        else:
            self._state = False
        
    async def async_turn_on(self, **kwargs):
        _LOGGER.debug("async_turn_on " + self._name + " " + str(self._brightness))
        self._state = True

        if ATTR_BRIGHTNESS in kwargs:
            self._brightness = kwargs[ATTR_BRIGHTNESS]
            
        if (self._dcsys_max) <= 1:
            self._brightness = 255
        
        await self.hass.async_add_executor_job(self.doActon)
            
        self.async_schedule_update_ha_state(True)

    async def async_turn_off(self, **kwargs):
        _LOGGER.info("async_turn_off " + self._name + " " + str(self._brightness))
        self._state = False
        await self.hass.async_add_executor_job(self.doActon)
        self.async_schedule_update_ha_state(True)

    @property
    def device_info(self):
        _LOGGER.info("device_info " + self._unique_id )
        return {
            "identifiers": {
                (DOMAIN, "dcsys_lichten_device")
            },
            "name": "DCSys lichten device",
            "manufacturer": "Struyve",
            "model": "DCSys licht",
            "sw_version": "0.1",
        }
        
    @property
    def name(self) -> str:
        return self._name

    @property
    def brightness(self):
        _LOGGER.debug("Brightness " + self._name + " " + str(self._brightness))
        return self._brightness

    @property
    def is_on(self) -> bool | None:
        _LOGGER.debug("is_on " + self._name)
        return self._state

    @property
    def should_poll(self):
        return True

    @property
    def supported_features(self):
        if self._dcsys_max > 1:
            return SUPPORT_BRIGHTNESS
        else:
            return 0

    @property
    def unique_id(self) -> str:
        return self._unique_id
