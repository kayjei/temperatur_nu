"""
A sensor created to read temperature from temperatur.nu
For more details about this platform, please refer to the documentation at
https://github.com/kayjei/temperatur_nu
"""
import logging
import json
import voluptuous as vol
import datetime
import secrets
import requests
import xmltodict

from homeassistant.helpers.entity import Entity
import homeassistant.helpers.config_validation as cv
from homeassistant.components.sensor import PLATFORM_SCHEMA
from homeassistant.const import CONF_NAME
from homeassistant.const import TEMP_CELSIUS
from homeassistant.util import Throttle

_LOGGER = logging.getLogger(__name__)

UPDATE_INTERVAL = datetime.timedelta(minutes=10)

PLATFORM_SCHEMA = PLATFORM_SCHEMA.extend({
    vol.Required(CONF_NAME): cv.ensure_list,
})

rand = secrets.token_hex(4)
BASE_URL = 'http://api.temperatur.nu/tnu_1.15.php?verbose&cli=homeassistant_' + rand
PERS_JSON = '.temperatur_nu.json'

def setup_platform(hass, config, add_devices, discovery_info=None):
    """Set up the sensor platform"""
    path = ''

    ent_list = config.get(CONF_NAME)
    for e in ent_list:
        path = path + str(e) + ','
        _LOGGER.debug("Entity from list: " + e)

    if len(ent_list) > 0:
        uri = "&p=" + str(path[:-1])
        URL = BASE_URL + uri
    else:
        _LOGGER.info("No sensors added in configuration.yaml")

    _LOGGER.debug("Created URL: " + URL)
    
    ApiRequest.call(URL)
    devices = []

    json_obj = ReadJson().json_data()

    try:
        poller_entity = json_obj["rss"]["channel"]["item"][0]["id"]
        _LOGGER.debug("Creating poller device: " + poller_entity)

        for res in json_obj["rss"]["channel"]["item"]:
            friendly_name = res["title"]
            sensor_id = res["id"]
            temp = res["temp"]
            lat = res["lat"]
            lon = res["lon"]
            lastUpdate = res["lastUpdate"]
            _LOGGER.debug("New sensor: " + str(friendly_name))

            devices.append(SensorDevice(sensor_id, None, lat, lon, lastUpdate, friendly_name, poller_entity, URL))
            _LOGGER.info("Adding sensor: " + str(sensor_id))

        add_devices(devices)

    except KeyError:
        _LOGGER.info(json_obj["rss"]["channel"]["item"]["title"])

class SensorDevice(Entity):
    def __init__(self, id, temperature, latitude, longitude, timestamp, name, poller_entity, url):
        if id.endswith("_"):
            self._device_id = str(id[:-1].lower().replace("\xe5","a").replace("\xe4","a").replace("\xf6","o").replace("-", "_").replace(".","").replace("___","_"))
        else:
            self._device_id = str(id.lower().replace("\xe5","a").replace("\xe4","a").replace("\xf6","o").replace("-", "_").replace(".","").replace("___","_"))
        self._state = temperature
        if id.endswith("_"):
            self._entity_id = 'sensor.temp_nu_' + str(id[:-1].lower().replace("\xe5","a").replace("\xe4","a").replace("\xf6","o").replace("-", "_").replace(".","").replace("___","_"))
        else:
            self._entity_id = 'sensor.temp_nu_' + str(id.lower().replace("\xe5","a").replace("\xe4","a").replace("\xf6","o").replace("-", "_").replace(".","").replace("___","_"))
        self._latitude = latitude
        self._longitude = longitude
        self._timestamp = timestamp
        self._friendly_name = name
        self._poller = poller_entity
        self._url = url
        self.update()

    @Throttle(UPDATE_INTERVAL)
    def update(self):
        """Temperature"""

        if self._device_id == self._poller:
            ApiRequest.call(self._url)

        jsonr = ReadJson().json_data()
        try:
            for ent in jsonr["rss"]["channel"]["item"]:
                if ent["id"].endswith("_"):
                    if ent["id"][:-1].lower().replace("\xe5","a").replace("\xe4","a").replace("\xf6","o").replace("-", "_").replace(".","").replace("___","_") == self._device_id:
                        if ent["temp"] == 'N/A':
                            self._state = None
                        else:
                            self._state = round(float(ent["temp"]), 1)
                elif ent["id"].lower().replace("\xe5","a").replace("\xe4","a").replace("\xf6","o").replace("-", "_").replace(".","").replace("___","_") == self._device_id:
                    if ent["temp"] == 'N/A':
                        self._state = None
                    else:
                        self._state = round(float(ent["temp"]), 1)
                    
                    self._timestamp = ent["lastUpdate"]
                    _LOGGER.debug("Temp is " + str(self._state) + " for " + str(self._friendly_name))

        except KeyError:
            _LOGGER.info(json_obj["rss"]["channel"]["item"]["title"])

    @property
    def entity_id(self):
        """Return the id of the sensor"""
        return self._entity_id
        _LOGGER.debug("Updating device " + self._entity_id)

    @property
    def unit_of_measurement(self) -> str:
        """Return the unit of measurement."""
        return '°C'

    @property
    def name(self):
        """Return the name of the sensor"""
        return self._friendly_name

    @property
    def temperature_unit(self):
        """Return the unit of measurement."""
        return TEMP_CELSIUS

    @property
    def state(self):
        """Return the state of the sensor"""
        return self._state

    @property
    def icon(self):
        """Return the icon of the sensor"""
        return 'mdi:thermometer'

    @property
    def device_class(self):
        """Return the device class of the sensor"""
        return 'temperature'

    @property
    def device_state_attributes(self):
        """Return the attribute(s) of the sensor"""
        return {
            "latitude": self._latitude,
            "longitude": self._longitude,
            "lastUpdate": self._timestamp,
            "source": "temperatur.nu"
            }

class ApiRequest:

    def call(url):
        """Temperature"""

        response = requests.get(url)

        if response.status_code == 200:
            xmlObj = xmltodict.parse(response.content)
            _LOGGER.debug("Sending API request to: " + url + " Printing result to " + PERS_JSON)
        
            with open(PERS_JSON, "w") as json_file:
                json.dump(xmlObj, json_file)

            return True

        else:
            return False

class ReadJson:
    def __init__(self):
        self.update()

    @Throttle(UPDATE_INTERVAL)
    def update(self):
        """Temperature"""
        _LOGGER.debug("Reading " + PERS_JSON + " for device")
        with open(PERS_JSON, "r") as json_file:
            json_datas = json.load(json_file)
        self._json_response = json_datas

    def json_data(self):
        """Keep json data"""
        return self._json_response
