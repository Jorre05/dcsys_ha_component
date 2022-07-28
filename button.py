from __future__ import annotations

from homeassistant.components import persistent_notification
from homeassistant.components.button import ButtonEntity
from homeassistant.config_entries import ConfigEntry
from homeassistant.const import DEVICE_DEFAULT_NAME
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.helpers.typing import ConfigType, DiscoveryInfoType

from .const import DOMAIN, GLOBAL_PARALLEL_UPDATES
from .dcsyslib import *

_LOGGER = logging.getLogger(__name__)
dcsys_knoppen = []
hostname = ""

async def async_setup_platform(hass, config, async_add_entities, discovery_info=None):
    _LOGGER.info("DCSys knop async_setup_platform gestart.")

async def async_setup_entry(hass, entry, async_add_devices):
    _LOGGER.info("DCSys knop async_setup_entry gestart.")
    async_add_devices(dcsys_knoppen)

def setHostname(h):
    global hostname
    hostname = h

class DcsysKnop(ButtonEntity):

    _attr_should_poll = False

    def __init__(self, name: str, seq_id: str) -> None:
        self._dcsys_seq_id = seq_id
        self._attr_unique_id = (name + "_" + seq_id).replace(" ", "_")
        self._attr_name = name

    async def async_press(self) -> None:
        _LOGGER.info("async_press " + self._attr_name + " io:" + self._dcsys_seq_id)
        await self.hass.async_add_executor_job(self.doUpdate)
        
    def doUpdate(self) -> None:
        global hostname
        execSequence(hostname, self._dcsys_seq_id,"")
            
    @property
    def device_info(self):
        _LOGGER.info("device_info " + self._attr_unique_id)
        return {
            "identifiers": {(DOMAIN, "dcsys_knoppen_device")},
            "name": "DCSys knoppen device",
            "manufacturer": "Struyve",
            "model": "DCSys knop",
            "sw_version": "0.1",
        }
