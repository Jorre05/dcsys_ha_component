"""Platform for light integration."""
from __future__ import annotations

import logging
from datetime import timedelta

import voluptuous as vol

import homeassistant.helpers.config_validation as cv
from homeassistant.components.climate import ClimateEntity, PLATFORM_SCHEMA
from homeassistant.components.climate.const import ATTR_HVAC_MODE, ATTR_TARGET_TEMP_HIGH, ATTR_TARGET_TEMP_LOW, HVAC_MODE_HEAT, HVAC_MODES, SUPPORT_TARGET_TEMPERATURE, CURRENT_HVAC_IDLE, CURRENT_HVAC_HEAT
from homeassistant.const import ATTR_TEMPERATURE, TEMP_CELSIUS
from homeassistant.core import HomeAssistant
from homeassistant.helpers.dispatcher import async_dispatcher_connect
from homeassistant.helpers.restore_state import RestoreEntity
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.helpers.typing import ConfigType, DiscoveryInfoType

from .const import DOMAIN, GLOBAL_PARALLEL_UPDATES
from .dcsyslib import *

_LOGGER = logging.getLogger(__name__)
PARALLEL_UPDATES = GLOBAL_PARALLEL_UPDATES
SCAN_INTERVAL = timedelta(seconds=10)
dcsys_thermostaten = []
hostname = ""

async def async_setup_platform(hass, config, async_add_entities, discovery_info=None):
    _LOGGER.info("DCSys thermostaten async_setup_platform gestart.")
    
async def async_setup_entry(hass, entry, async_add_devices):
    _LOGGER.info("DCSys thermostaten setup entry gestart!")
    async_add_devices(dcsys_thermostaten)

def setHostname(h):
    global hostname
    hostname = h
    
class DcsysThermostaat(ClimateEntity,RestoreEntity):
    
    def __init__(self,name,io_id,rad_id,status,min,max,step,seq_set) -> None:
        self._name = name
        _LOGGER.info("Init " + self._name)

        self._dcsys_io_id = io_id
        self._dcsys_rad_id = rad_id
        self._dcsys_seq_set = seq_set
        self._dcsys_raw_value = 0.0

        self._state = status
        self._unique_id = (name + "_" + io_id).replace(" ", "_")
        
        l = []
        l.append(HVAC_MODE_HEAT)
        self._hvac_modes = l
        self._hvac_mode = HVAC_MODE_HEAT
        self._hvac_action = CURRENT_HVAC_IDLE
        self._temperature_unit = TEMP_CELSIUS
        self._current_temperature = None
        self._target_temperature = None
        self._target_temperature_step = step
        self._target_temperature_high = max
        self._target_temperature_low = min
        self._min_temp = min
        self._max_temp = max

    def doSetSwo(self) -> None:
        _LOGGER.debug("doSetSwo " + self._name)
        global hostname
        
        execSequence(hostname,self._dcsys_seq_set,self._target_temperature)
        
    def doUpdate(self) -> None:
        _LOGGER.debug("doUpdate " + self._name)
        global hostname
        self._current_temperature = float(getIoCalculatedValue(hostname,self._dcsys_io_id))
        self._target_temperature = float(getIoSwoCalculatedValue(hostname,self._dcsys_io_id))
        radiator_status =  int(getIoRawValue(hostname,self._dcsys_rad_id))
        if radiator_status == 0:
            self._hvac_action = CURRENT_HVAC_IDLE
        else:
            self._hvac_action = CURRENT_HVAC_HEAT
        
    async def async_update(self) -> None:
        _LOGGER.debug("async_update " + self._name)
        await self.hass.async_add_executor_job(self.doUpdate)
        
    async def async_set_hvac_mode(self, hvac_mode: str) -> None:
        _LOGGER.debug("DCSys set thermostaat mode naar : " + hvac_mode)
        if hvac_mode in self._hvac_modes:
            self._attr_hvac_mode = hvac_mode
            await self.async_update_ha_state()

    async def async_set_temperature(self, **kwargs):
        if ATTR_TARGET_TEMP_HIGH in kwargs:
            self._target_temperature_high = kwargs[ATTR_TARGET_TEMP_HIGH]

        if ATTR_TARGET_TEMP_LOW in kwargs:
            self._target_temperature_lo = kwargs[ATTR_TARGET_TEMP_LOW]

        if ATTR_TEMPERATURE in kwargs:
            _LOGGER.debug("DCSys thermostaat temp : " + str(kwargs[ATTR_TEMPERATURE]))
            self._target_temperature = kwargs[ATTR_TEMPERATURE]

        await self.hass.async_add_executor_job(self.doSetSwo)

    async def async_turn_on(self, **kwargs):
        _LOGGER.debug("async_turn_on " + self._name)
        self._state = True
        self.async_schedule_update_ha_state()

    async def async_turn_off(self, **kwargs):
        _LOGGER.debug("async_turn_off " + self._name)
        self._state = False
        self.async_schedule_update_ha_state()

    async def async_added_to_hass(self) -> None:
        _LOGGER.debug("async_added_to_hass " + self._name)
        await super().async_added_to_hass()
        await self.hass.async_add_executor_job(self.doUpdate)

    @property
    def device_info(self):
        _LOGGER.debug("device_info " + self._unique_id )
        return {
            "identifiers": {
                (DOMAIN, "dcsys_thermostaten_device")
            },
            "name": "DCSys thermostaten device",
            "manufacturer": "Struyve",
            "model": "DCSys thermostaat",
            "sw_version": "0.1",
        }

    @property
    def name(self) -> str:
        return self._name

    @property
    def is_on(self) -> bool | None:
        return self._state

    @property
    def should_poll(self):
        return True

    @property
    def supported_features(self):
        return SUPPORT_TARGET_TEMPERATURE
        
    @property
    def temperature_unit(self) -> str:
        return self._temperature_unit
        
    @property
    def hvac_modes(self) -> list[str]:
        return self._hvac_modes
        
    @property
    def unique_id(self) -> str:
        return self._unique_id

    @property
    def current_temperature(self) -> float | None:
        _LOGGER.debug("DCSys get current :" + str(self._current_temperature))
        return self._current_temperature

    @property
    def target_temperature(self) -> float | None:
        _LOGGER.debug("DCSys target_temperature :" + str(self._target_temperature))
        return self._target_temperature

    @property
    def target_temperature_step(self) -> float | None:
        _LOGGER.debug("DCSys get step :" + str(self._target_temperature_step))
        return self._target_temperature_step

    @property
    def target_temperature_high(self) -> float | None:
        _LOGGER.debug("DCSys get high :" + str(self._target_temperature_high))
        return self._target_temperature_high

    @property
    def target_temperature_low(self) -> float | None:
        _LOGGER.debug("DCSys get low :" + str(self._target_temperature_low))
        return self._target_temperature_low

    @property
    def min_temp(self) -> float:
        _LOGGER.debug("DCSys min_temp :" + str(self._min_temp))
        return self._min_temp

    @property
    def max_temp(self) -> float:
        _LOGGER.debug("DCSys max_temp :" + str(self._max_temp))
        return self._max_temp

    @property
    def hvac_mode(self) -> str:
        _LOGGER.debug("DCSys get thermostaat mode")
        return self._hvac_mode
    
    @property
    def hvac_action(self) -> str | None:
        _LOGGER.debug("DCSys get thermostaat action : " + self._hvac_action)
        return self._hvac_action
