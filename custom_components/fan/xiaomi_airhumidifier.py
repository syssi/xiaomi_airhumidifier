"""
Support for Xiaomi Mi Air Humidifier.

"""
import asyncio
from functools import partial
import logging

import voluptuous as vol

from homeassistant.helpers.entity import ToggleEntity
from homeassistant.components.fan import (FanEntity, PLATFORM_SCHEMA,
                                          SUPPORT_SET_SPEED, DOMAIN, )
from homeassistant.const import (CONF_NAME, CONF_HOST, CONF_TOKEN,
                                 ATTR_ENTITY_ID, )
from homeassistant.exceptions import PlatformNotReady
import homeassistant.helpers.config_validation as cv

_LOGGER = logging.getLogger(__name__)

DEFAULT_NAME = 'Xiaomi Air Purifier'
PLATFORM = 'xiaomi_miio'

PLATFORM_SCHEMA = PLATFORM_SCHEMA.extend({
    vol.Required(CONF_HOST): cv.string,
    vol.Required(CONF_TOKEN): vol.All(cv.string, vol.Length(min=32, max=32)),
    vol.Optional(CONF_NAME, default=DEFAULT_NAME): cv.string,
})

REQUIREMENTS = ['python-miio==0.3.5']

ATTR_TEMPERATURE = 'temperature'
ATTR_HUMIDITY = 'humidity'
ATTR_MODE = 'mode'
ATTR_BUZZER = 'buzzer'
ATTR_LED_BRIGHTNESS = 'led_brightness'
ATTR_BRIGHTNESS = 'brightness'
ATTR_CHILD_LOCK = 'child_lock'
ATTR_TARGET_HUMIDITY = 'target_humidity'
ATTR_TRANS_LEVEL = 'trans_level'

SUCCESS = ['ok']

SERVICE_SET_BUZZER_ON = 'xiaomi_miio_set_buzzer_on'
SERVICE_SET_BUZZER_OFF = 'xiaomi_miio_set_buzzer_off'
SERVICE_SET_CHILD_LOCK_ON = 'xiaomi_miio_set_child_lock_on'
SERVICE_SET_CHILD_LOCK_OFF = 'xiaomi_miio_set_child_lock_off'
SERVICE_SET_TARGET_HUMIDITY = 'xiaomi_miio_set_target_humidity'
SERVICE_SET_LED_BRIGHTNESS = 'xiaomi_miio_set_led_brightness'

AIRPURIFIER_SERVICE_SCHEMA = vol.Schema({
    vol.Optional(ATTR_ENTITY_ID): cv.entity_ids,
})

SERVICE_SCHEMA_LED_BRIGHTNESS = AIRPURIFIER_SERVICE_SCHEMA.extend({
    vol.Required(ATTR_BRIGHTNESS):
        vol.All(vol.Coerce(int), vol.Clamp(min=0, max=2))
})

SERVICE_SCHEMA_TARGET_HUMIDITY = AIRPURIFIER_SERVICE_SCHEMA.extend({
    vol.Required(ATTR_HUMIDITY):
        vol.All(vol.Coerce(int), vol.In([30, 40, 50, 60, 70, 80]))
})

SERVICE_TO_METHOD = {
    SERVICE_SET_BUZZER_ON: {'method': 'async_set_buzzer_on'},
    SERVICE_SET_BUZZER_OFF: {'method': 'async_set_buzzer_off'},
    SERVICE_SET_CHILD_LOCK_ON: {'method': 'async_set_child_lock_on'},
    SERVICE_SET_CHILD_LOCK_OFF: {'method': 'async_set_child_lock_off'},
    SERVICE_SET_TARGET_HUMIDITY: {
        'method': 'async_set_target_humidity',
        'schema': SERVICE_SCHEMA_TARGET_HUMIDITY},
    SERVICE_SET_LED_BRIGHTNESS: {
        'method': 'async_set_led_brightness',
        'schema': SERVICE_SCHEMA_LED_BRIGHTNESS},
}


# pylint: disable=unused-argument
@asyncio.coroutine
def async_setup_platform(hass, config, async_add_devices, discovery_info=None):
    """Set up the air humidifier from config."""
    from miio import AirHumidifier, DeviceException
    if PLATFORM not in hass.data:
        hass.data[PLATFORM] = {}

    host = config.get(CONF_HOST)
    name = config.get(CONF_NAME)
    token = config.get(CONF_TOKEN)

    _LOGGER.info("Initializing with host %s (token %s...)", host, token[:5])

    try:
        air_humidifier = AirHumidifier(host, token)

        xiaomi_air_humidifier = XiaomiAirHumidifier(name, air_humidifier)
        hass.data[PLATFORM][host] = xiaomi_air_humidifier
    except DeviceException:
        raise PlatformNotReady

    async_add_devices([xiaomi_air_humidifier], update_before_add=True)

    @asyncio.coroutine
    def async_service_handler(service):
        """Map services to methods on XiaomiAirHumidifier."""
        method = SERVICE_TO_METHOD.get(service.service)
        params = {key: value for key, value in service.data.items()
                  if key != ATTR_ENTITY_ID}
        entity_ids = service.data.get(ATTR_ENTITY_ID)
        if entity_ids:
            devices = [device for device in hass.data[PLATFORM].values() if
                       device.entity_id in entity_ids]
        else:
            devices = hass.data[PLATFORM].values()

        update_tasks = []
        for device in devices:
            yield from getattr(device, method['method'])(**params)
            update_tasks.append(device.async_update_ha_state(True))

        if update_tasks:
            yield from asyncio.wait(update_tasks, loop=hass.loop)

    for air_humidifier_service in SERVICE_TO_METHOD:
        schema = SERVICE_TO_METHOD[air_humidifier_service].get(
            'schema', AIRPURIFIER_SERVICE_SCHEMA)
        hass.services.async_register(DOMAIN, air_humidifier_service,
                                     async_service_handler, schema=schema)


class XiaomiAirHumidifier(FanEntity):
    """Representation of a Xiaomi Air Purifier."""

    def __init__(self, name, air_humidifier):
        """Initialize the air humidifier."""
        self._name = name

        self._air_humidifier = air_humidifier
        self._state = None
        self._state_attrs = {
            ATTR_TEMPERATURE: None,
            ATTR_HUMIDITY: None,
            ATTR_MODE: None,
            ATTR_BUZZER: None,
            ATTR_LED_BRIGHTNESS: None,
            ATTR_CHILD_LOCK: None,
            ATTR_TRANS_LEVEL: None,
            ATTR_TARGET_HUMIDITY: None,
        }

    @property
    def supported_features(self):
        """Flag supported features."""
        return SUPPORT_SET_SPEED

    @property
    def should_poll(self):
        """Poll the fan."""
        return True

    @property
    def name(self):
        """Return the name of the device if any."""
        return self._name

    @property
    def available(self):
        """Return true when state is known."""
        return self._state is not None

    @property
    def device_state_attributes(self):
        """Return the state attributes of the device."""
        return self._state_attrs

    @property
    def is_on(self):
        """Return true if fan is on."""
        return self._state

    @asyncio.coroutine
    def _try_command(self, mask_error, func, *args, **kwargs):
        """Call a air humidifier command handling error messages."""
        from miio import DeviceException
        try:
            result = yield from self.hass.async_add_job(
                partial(func, *args, **kwargs))

            _LOGGER.debug("Response received from air humidifier: %s", result)

            return result == SUCCESS
        except DeviceException as exc:
            _LOGGER.error(mask_error, exc)
            return False

    @asyncio.coroutine
    def async_turn_on(self: ToggleEntity, speed: str=None, **kwargs) -> None:
        """Turn the fan on."""
        if speed:
            # If operation mode was set the device must not be turned on.
            yield from self.async_set_speed(speed)
            return

        yield from self._try_command(
            "Turning the air humidifier on failed.", self._air_humidifier.on)

    @asyncio.coroutine
    def async_turn_off(self: ToggleEntity, **kwargs) -> None:
        """Turn the fan off."""
        yield from self._try_command(
            "Turning the air humidifier off failed.", self._air_humidifier.off)

    @asyncio.coroutine
    def async_update(self):
        """Fetch state from the device."""
        from miio import DeviceException

        try:
            state = yield from self.hass.async_add_job(
                self._air_humidifier.status)
            _LOGGER.debug("Got new state: %s", state)

            self._state = state.is_on
            self._state_attrs = {
                ATTR_TEMPERATURE: state.temperature,
                ATTR_HUMIDITY: state.humidity,
                ATTR_MODE: state.mode.value,
                ATTR_BUZZER: state.buzzer,
                ATTR_CHILD_LOCK: state.child_lock,
                ATTR_TRANS_LEVEL: state.trans_level,
                ATTR_TARGET_HUMIDITY: state.target_humidity,
            }

            if state.led_brightness:
                self._state_attrs[
                    ATTR_LED_BRIGHTNESS] = state.led_brightness.value

        except DeviceException as ex:
            _LOGGER.error("Got exception while fetching the state: %s", ex)

    @property
    def speed_list(self: ToggleEntity) -> list:
        """Get the list of available speeds."""
        from miio.airhumidifier import OperationMode
        return [mode.name for mode in OperationMode]

    @property
    def speed(self):
        """Return the current speed."""
        if self._state:
            from miio.airhumidifier import OperationMode

            return OperationMode(self._state_attrs[ATTR_MODE]).name

        return None

    @asyncio.coroutine
    def async_set_speed(self: ToggleEntity, speed: str) -> None:
        """Set the speed of the fan."""
        _LOGGER.debug("Setting the operation mode to: " + speed)
        from miio.airhumidifier import OperationMode

        yield from self._try_command(
            "Setting operation mode of the air humidifier failed.",
            self._air_humidifier.set_mode, OperationMode[speed])

    @asyncio.coroutine
    def async_set_buzzer_on(self):
        """Turn the buzzer on."""
        yield from self._try_command(
            "Turning the buzzer of the air humidifier on failed.",
            self._air_humidifier.set_buzzer, True)

    @asyncio.coroutine
    def async_set_buzzer_off(self):
        """Turn the buzzer off."""
        yield from self._try_command(
            "Turning the buzzer of the air humidifier off failed.",
            self._air_humidifier.set_buzzer, False)

    @asyncio.coroutine
    def async_set_child_lock_on(self):
        """Turn the child lock on."""
        yield from self._try_command(
            "Turning the child lock of the air humidifier on failed.",
            self._air_humidifier.set_child_lock, True)

    @asyncio.coroutine
    def async_set_child_lock_off(self):
        """Turn the child lock off."""
        yield from self._try_command(
            "Turning the child lock of the air humidifier off failed.",
            self._air_humidifier.set_child_lock, False)

    @asyncio.coroutine
    def async_set_led_brightness(self, brightness: int=2):
        """Set the led brightness."""
        from miio.airhumidifier import LedBrightness

        yield from self._try_command(
            "Setting the led brightness of the air humidifier failed.",
            self._air_humidifier.set_led_brightness, LedBrightness(brightness))

    @asyncio.coroutine
    def async_set_target_humidity(self, humidity: int=40):
        """Set the target humidity."""
        yield from self._try_command(
            "Setting the target humidity of the air humidifier failed.",
            self._air_humidifier.set_target_humidity, humidity)
