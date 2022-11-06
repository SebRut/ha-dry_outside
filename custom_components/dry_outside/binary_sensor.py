"""Binary sensor platform for integration_blueprint."""
from typing import Optional

from homeassistant.components.binary_sensor import BinarySensorEntity
from homeassistant.components.weather import (
    ATTR_WEATHER_HUMIDITY,
    ATTR_WEATHER_TEMPERATURE,
)
from homeassistant.const import EVENT_HOMEASSISTANT_START, TEMP_CELSIUS
from homeassistant.core import callback
from homeassistant.exceptions import HomeAssistantError
from homeassistant.helpers.event import async_track_state_change
from homeassistant.util.temperature import convert as convert_temperature

from . import should_dry_outside
from .const import BINARY_SENSOR, BINARY_SENSOR_DEVICE_CLASS, DEFAULT_NAME, DOMAIN, ICON
from .entity import DryOutsideEntity


async def async_setup_entry(hass, entry, async_add_devices):
    """Setup binary_sensor platform."""
    coordinator = hass.data[DOMAIN][entry.entry_id]
    async_add_devices([DryOutsideBinarySensor(coordinator, entry)])


class DryOutsideBinarySensor(DryOutsideEntity, BinarySensorEntity):
    def __init__(self, coordinator, config_entry):
        super().__init__(coordinator, config_entry)

    @property
    def should_poll(self) -> bool:
        return False

    @property
    def name(self):
        """Return the name of the binary_sensor."""
        return f"{DEFAULT_NAME}_{BINARY_SENSOR}"

    @property
    def icon(self) -> str | None:
        return ICON

    @property
    def available(self) -> bool:
        return self.is_on is not None

    @property
    def device_class(self):
        return BINARY_SENSOR_DEVICE_CLASS

    async def async_added_to_hass(self):
        @callback
        def sensor_state_listener(entity, old_state, new_state):
            self.async_schedule_update_ha_state(True)

        @callback
        def sensor_startup(event):
            async_track_state_change(
                self.hass, [self.config_entry.weather_entity], sensor_state_listener
            )

            self.async_schedule_update_ha_state(True)

        self.hass.bus.async_listen_once(EVENT_HOMEASSISTANT_START, sensor_startup)

    @staticmethod
    def _temp2c(temperature: Optional[float], temperature_unit: str) -> Optional[float]:
        """Convert weather temperature to Celsius degree."""
        if temperature is not None and temperature_unit != TEMP_CELSIUS:
            temperature = convert_temperature(
                temperature, temperature_unit, TEMP_CELSIUS
            )

        return temperature

    async def async_update(self):
        weather_data = self.hass.states.get(self.config_entry.weather_entity)

        if weather_data is None:
            raise HomeAssistantError(
                f"Unable to find an entity called {self.config_entry.weather_entity}"
            )

        temp_unit = self.hass.config.units.temperature_unit
        temp = weather_data.attributes.get(ATTR_WEATHER_TEMPERATURE)
        temp_c = self._temp2c(temp, temp_unit)

        humidity = weather_data.attributes.get(ATTR_WEATHER_HUMIDITY)
        # TODO _LOGGER.debug("Current temperature %s, humidity %s", temp, humidity)

        dry_outside = await should_dry_outside(temp_c, humidity)

        self._attr_is_on = dry_outside
