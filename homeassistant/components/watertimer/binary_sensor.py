from typing import Callable, Iterable

from homeassistant.components.binary_sensor import (
    DEVICE_CLASS_MOVING,
    DEVICE_CLASS_RUNNING,
    DOMAIN as SENSOR_DOMAIN,
    BinarySensorEntity,
)
from homeassistant.config_entries import ConfigEntry
from homeassistant.const import Platform
from homeassistant.core import HomeAssistant
from homeassistant.helpers.device_registry import format_mac
from homeassistant.helpers.entity import Entity
from homeassistant.helpers.entity_platform import AddEntitiesCallback

from .const import DOMAIN
from .device_wrapper import WaterTimerDevice


async def async_setup_entry(
    hass: HomeAssistant, entry: ConfigEntry, add_entities_callback: AddEntitiesCallback
) -> bool:
    device = WaterTimerDevice(entry.data["mac"])
    add_entities_callback(
        [WaterTimerRunningStatus(entry, device), WaterTimerAutoStatus(entry, device)]
    )
    return True


class WaterTimerRunningStatus(BinarySensorEntity):
    def __init__(self, entry: ConfigEntry, device: WaterTimerDevice):
        self._dev = device
        self._attr_device_class = DEVICE_CLASS_RUNNING
        self._integration_name = entry.title
        self.entity_id = (
            f"{SENSOR_DOMAIN}.{DOMAIN}.{format_mac(self._dev.mac)}.running-state"
        )

    @property
    def device_info(self):
        return {
            "identifiers": {(DOMAIN, self._dev.mac)},
            "name": self._integration_name,
            # "manufacturer": self.light.manufacturername,
            # "model": self.light.productname,
            # "sw_version": self.light.swversion,
            # "via_device": (hue.DOMAIN, self.api.bridgeid),
        }

    @property
    def name(self):
        """Name of the entity."""
        return f"Running state of {self._integration_name}"

    @property
    def is_on(self):
        """If the switch is currently on or off."""
        return self._dev.is_running

    @property
    def unique_id(self) -> str:
        return f"{format_mac(self._dev.mac)}.running-state"


class WaterTimerAutoStatus(BinarySensorEntity):
    def __init__(self, entry: ConfigEntry, device: WaterTimerDevice):
        self._dev = device
        self._attr_device_class = DEVICE_CLASS_MOVING
        self._integration_name = entry.title
        self.entity_id = (
            f"{SENSOR_DOMAIN}.{DOMAIN}.{format_mac(self._dev.mac)}.auto-mode-on"
        )

    @property
    def device_info(self):
        return {
            "identifiers": {(DOMAIN, self._dev.mac)},
            "name": self._integration_name,
            # "manufacturer": self.light.manufacturername,
            # "model": self.light.productname,
            # "sw_version": self.light.swversion,
            # "via_device": (hue.DOMAIN, self.api.bridgeid),
        }

    @property
    def name(self):
        """Name of the entity."""
        return f"Auto mode state of {self._integration_name}"

    @property
    def is_on(self):
        """If the switch is currently on or off."""
        return self._dev.is_auto_mode_on

    @property
    def unique_id(self) -> str:
        return f"{format_mac(self._dev.mac)}.auto-mode-on"
