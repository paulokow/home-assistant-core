"""
"""
from homeassistant.components.sensor import (
    DOMAIN as SENSOR_DOMAIN,
    SensorDeviceClass,
    SensorEntity,
    SensorStateClass,
)
from homeassistant.config_entries import ConfigEntry
from homeassistant.const import PERCENTAGE
from homeassistant.core import HomeAssistant
from homeassistant.helpers.device_registry import format_mac
from homeassistant.helpers.entity_platform import AddEntitiesCallback

from .const import DOMAIN
from .device_wrapper import WaterTimerDevice


async def async_setup_entry(
    hass: HomeAssistant, entry: ConfigEntry, add_entities_callback: AddEntitiesCallback
) -> None:
    """Function which is called by HAAS to setup entities of this platform

    :param hass: reference to HASS
    :type hass: HomeAssistant
    :param entry: configuration
    :type entry: ConfigEntry
    :param add_entities_callback: callback function to add entities
    :type add_entities_callback: AddEntitiesCallback
    :return: success
    :rtype: bool
    """
    device = WaterTimerDevice(entry.data["mac"], entry.title)
    add_entities_callback([WaterTimerBatteryStatus(entry, device)])


class WaterTimerBatteryStatus(SensorEntity):
    """_summary_

    :param BinarySensorEntity: _description_
    :type BinarySensorEntity: _type_
    """

    _attr_state_class = SensorStateClass.MEASUREMENT
    _attr_device_class = SensorDeviceClass.BATTERY
    _attr_native_unit_of_measurement = PERCENTAGE

    def __init__(self, entry: ConfigEntry, device: WaterTimerDevice) -> None:
        self._dev = device
        self._integration_name = entry.title
        self.entity_id = f"{SENSOR_DOMAIN}.{DOMAIN}.{format_mac(self._dev.mac)}.battery"

    @property
    def device_info(self):
        return self._dev.device_info

    @property
    def name(self):
        """Name of the entity."""
        return f"Battery level of {self._integration_name}"

    @property
    def unique_id(self) -> str:
        return f"{format_mac(self._dev.mac)}.battery"

    def update(self) -> None:
        self._dev.update()
        self._attr_native_value = self._dev.battery_level

    @property
    def available(self) -> bool:
        """Return True if entity is available."""
        return self._dev.available
