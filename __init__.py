"""This is my DCSys integration."""
import logging

from homeassistant.components.sensor import SensorDeviceClass
from homeassistant.const import CONF_HOST

from .const   import DOMAIN
from .light   import DcsysLicht       , dcsys_lichten      , setHostname as setLichtHostname
from .climate import DcsysThermostaat , dcsys_thermostaten , setHostname as setThermoHostname
from .sensor  import DcsysSensor      , dcsys_sensors      , setHostname as setSensoHostname
from .switch  import DcsysSchakelaar  , dcsys_schakelaars  , setHostname as setSchakelaarHostname
from .button  import DcsysKnop        , dcsys_knoppen      , setHostname as setKnopHostname

_LOGGER = logging.getLogger(__name__)

async def async_setup(hass, config):
    hass.states.async_set(DOMAIN + ".device", "DCSYS")

    if DOMAIN not in config:
        _LOGGER.info("Geen dcsys in configuration.yaml")
    else:
        _LOGGER.info("Wel dcsys in configuration.yaml")

    return True


async def async_setup_entry(hass, entry):
    _LOGGER.info("async_setup_entry entry.entry_id: " + entry.entry_id    )

    hass.data.setdefault(DOMAIN, {})
    hass.data[DOMAIN][entry.entry_id] = entry.data
    setThermoHostname(entry.data[CONF_HOST])
    setLichtHostname(entry.data[CONF_HOST])
    setSensoHostname(entry.data[CONF_HOST])
    setSchakelaarHostname(entry.data[CONF_HOST])
    setKnopHostname(entry.data[CONF_HOST])

    #                                Naam                    ,io_id  ,status ,minimum,maximum,step
    dcsys_lichten.append(DcsysLicht("Licht living boven"    , "1106", False, 0, 4095, 20))
    dcsys_lichten.append(DcsysLicht("Licht living beneden"  , "1105", False, 0, 4095, 20))
    dcsys_lichten.append(DcsysLicht("Licht keuken tafel"    , "1103", False, 0, 1, 1))
    dcsys_lichten.append(DcsysLicht("Licht keuken kasten"   , "1104", False, 0, 1, 1))
    dcsys_lichten.append(DcsysLicht("Licht hal beneden"     , "1102", False, 0, 1, 1))
    dcsys_lichten.append(DcsysLicht("Licht vestiaire"       , "1117", False, 0, 1, 1))
    dcsys_lichten.append(DcsysLicht("Licht wc"              , "1107", False, 0, 1, 1))
    dcsys_lichten.append(DcsysLicht("Licht waskot"          , "1108", False, 0, 1, 1))
    dcsys_lichten.append(DcsysLicht("Licht kelder"          , "1109", False, 0, 1, 1))
    dcsys_lichten.append(DcsysLicht("Licht buiten"          , "1101", False, 0, 1, 1))
    dcsys_lichten.append(DcsysLicht("Licht hal badkamer"    , "2103", False, 0, 1, 1))
    dcsys_lichten.append(DcsysLicht("Licht badkamer"        , "2109", False, 0, 1, 1))
    dcsys_lichten.append(DcsysLicht("Licht badkamer spiegel", "2110", False, 0, 1, 1))
    dcsys_lichten.append(DcsysLicht("Licht slaapkamer"      , "2101", False, 0, 4095, 20))
    dcsys_lichten.append(DcsysLicht("Licht Bureau luchter"  , "2102", False, 0, 1, 1))
    dcsys_lichten.append(DcsysLicht("Licht Bureau wand"     , "2104", False, 0, 1, 1))  # en 2105
    dcsys_lichten.append(DcsysLicht("Licht hal boven"       , "3101", False, 0, 1, 1))

    #                                           Naam                    ,io_id   ,rad_id ,status ,minimum,maximum,step,set_seq
    #dcsys_thermostaten.append(DcsysThermostaat("Temperatuur keuken"    , "11003", "12005", False, 5, 30, 0.1, "2003"))
    #dcsys_thermostaten.append(DcsysThermostaat("Temperatuur living"    , "11004", "12006", False, 5, 30, 0.1, "2004"))
    #dcsys_thermostaten.append(DcsysThermostaat("Temperatuur berging"   , "11006", "12001", False, 5, 30, 0.1, "2006"))
    #dcsys_thermostaten.append(DcsysThermostaat("Temperatuur badkamer"  , "11008", "12002", False, 5, 30, 0.1, "2008"))
    #dcsys_thermostaten.append(DcsysThermostaat("Temperatuur slaapkamer", "11001", "12003", False, 5, 30, 0.1, "2001"))
    dcsys_thermostaten.append(DcsysThermostaat("Thermostaat Tibo"      , "11007", "12004", False, 5, 30, 0.1, "2007"))
    #dcsys_thermostaten.append(DcsysThermostaat("Temperatuur Rani"      , "11010", "12008", False, 5, 30, 0.1, "2009"))
    #dcsys_thermostaten.append(DcsysThermostaat("Temperatuur Nele"      , "11009", "12007", False, 5, 30, 0.1, "2010"))
    #dcsys_thermostaten.append(DcsysThermostaat("Temperatuur bureau"    , "11002", "12009", False, 5, 30, 0.1, "2002"))

    #                                           Naam      , io_id  , devoce_class
    dcsys_sensors.append(DcsysSensor("Temperatuur buiten" , "11012", SensorDeviceClass.TEMPERATURE))
    dcsys_sensors.append(DcsysSensor("Temperatuur Tibo"   , "11007", SensorDeviceClass.TEMPERATURE))
    
    dcsys_sensors.append(DcsysSensor("Licht buiten"       , "11011", SensorDeviceClass.ILLUMINANCE))
    #dcsys_sensors.append(DcsysSensor("Electriciteit"      , "11011", SensorDeviceClass.ILLUMINANCE))

    #                               Naam                     ,io_id
    dcsys_schakelaars.append(DcsysSchakelaar("Stopcontact living kast" ,"1119"))
    dcsys_schakelaars.append(DcsysSchakelaar("Stopcontact living TV"   ,"1118"))
    dcsys_schakelaars.append(DcsysSchakelaar("Rolluiken master"   ,"10013"))
    dcsys_schakelaars.append(DcsysSchakelaar("Schauffage master"  ,"10001"))
    dcsys_schakelaars.append(DcsysSchakelaar("Stroom balanceren"  ,"20070"))
    
    # Radiators, status wordt in Esphome toestellen gebruikt.
    dcsys_schakelaars.append(DcsysSchakelaar("Radiator berging"    ,"12001"))
    dcsys_schakelaars.append(DcsysSchakelaar("Radiator badkamer"   ,"12002"))
    dcsys_schakelaars.append(DcsysSchakelaar("Radiator slaapkamer" ,"12003"))
    dcsys_schakelaars.append(DcsysSchakelaar("Radiator Tibo"       ,"12004"))
    dcsys_schakelaars.append(DcsysSchakelaar("Radiator keuken"     ,"12005"))
    dcsys_schakelaars.append(DcsysSchakelaar("Radiator living"     ,"12006"))
    dcsys_schakelaars.append(DcsysSchakelaar("Radiator Rani"       ,"12007"))
    dcsys_schakelaars.append(DcsysSchakelaar("Radiator Nele"       ,"12008"))
    dcsys_schakelaars.append(DcsysSchakelaar("Radiator bureau"     ,"12009"))
    
    #                               Naam                     ,seq_id
    dcsys_knoppen.append(DcsysKnop("Rolluiken omhoog" , "210"))
    dcsys_knoppen.append(DcsysKnop("Rolluiken omlaag" , "209"))
    dcsys_knoppen.append(DcsysKnop("Alle lichten uit" ,  "10"))
    dcsys_knoppen.append(DcsysKnop("Living sfeer 1"   ,"4010"))
    dcsys_knoppen.append(DcsysKnop("Toeter"           ,"1014"))
    dcsys_knoppen.append(DcsysKnop("Achterdeur dicht" ,"1015"))
    dcsys_knoppen.append(DcsysKnop("Achterdeur open"  ,"1016"))
    dcsys_knoppen.append(DcsysKnop("Nacht"            ,"2082"))
    
    # Radiator commando's, status wordt vanuit Esphome toestellen aangestuurd
    dcsys_knoppen.append(DcsysKnop("Radiator berging af"     ,"3009"))
    dcsys_knoppen.append(DcsysKnop("Radiator berging aan"    ,"3010"))
    dcsys_knoppen.append(DcsysKnop("Radiator badkamer af"    ,"3013"))
    dcsys_knoppen.append(DcsysKnop("Radiator badkamer aan"   ,"3014"))
    dcsys_knoppen.append(DcsysKnop("Radiator slaapkamer af"  ,"3001"))
    dcsys_knoppen.append(DcsysKnop("Radiator slaapkamer aan" ,"3002"))
    dcsys_knoppen.append(DcsysKnop("Radiator Tibo af"        ,"3011"))
    dcsys_knoppen.append(DcsysKnop("Radiator Tibo aan"       ,"3012"))
    dcsys_knoppen.append(DcsysKnop("Radiator keuken af"      ,"3005"))
    dcsys_knoppen.append(DcsysKnop("Radiator keuken aan"     ,"3006"))
    dcsys_knoppen.append(DcsysKnop("Radiator living af"      ,"3007"))
    dcsys_knoppen.append(DcsysKnop("Radiator living aan"     ,"3008"))
    dcsys_knoppen.append(DcsysKnop("Radiator Rani af"        ,"3017"))
    dcsys_knoppen.append(DcsysKnop("Radiator Rani aan"       ,"3018"))
    dcsys_knoppen.append(DcsysKnop("Radiator Nele af"        ,"3015"))
    dcsys_knoppen.append(DcsysKnop("Radiator Nele aan"       ,"3016"))
    dcsys_knoppen.append(DcsysKnop("Radiator bureau af"      ,"3003"))
    dcsys_knoppen.append(DcsysKnop("Radiator bureau aan"     ,"3004"))

    hass.async_add_job(hass.config_entries.async_forward_entry_setup(entry, "climate"))
    hass.async_add_job(hass.config_entries.async_forward_entry_setup(entry, "light"))
    hass.async_add_job(hass.config_entries.async_forward_entry_setup(entry, "sensor"))
    hass.async_add_job(hass.config_entries.async_forward_entry_setup(entry, "switch"))
    hass.async_add_job(hass.config_entries.async_forward_entry_setup(entry, "button"))

    return True
