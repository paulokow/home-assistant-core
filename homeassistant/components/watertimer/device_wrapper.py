from datetime import datetime, timedelta
import logging
from random import randint
from time import sleep
from typing import Union

from spraymistf638.driver import RunningMode, SprayMistF638, WorkingMode

from .const import DOMAIN

_LOGGER = logging.getLogger(__name__)

if _LOGGER.isEnabledFor(logging.DEBUG):
    from unittest.mock import Mock, PropertyMock

    SprayMistF638 = Mock(spec=SprayMistF638)
    SprayMistF638.return_value.connect = Mock(side_effect=lambda: randint(0, 3) != 0)
    type(SprayMistF638.return_value).running_mode = PropertyMock(
        side_effect=lambda: randint(0, 3)
    )
    type(SprayMistF638.return_value).working_mode = PropertyMock(
        side_effect=lambda: randint(0, 1)
    )
    type(SprayMistF638.return_value).battery_level = PropertyMock(
        side_effect=lambda: randint(1, 100)
    )
    _LOGGER.warning("Device is mocked in debug logging mode")


class WaterTimerDevice:
    """AI is creating summary for"""

    def __init__(self, mac: str, name: str) -> None:
        self._mac = mac
        self._last_update = datetime.min
        self._name = name
        self._is_available = False
        self._is_running = False
        self._battery_level = None
        self._auto_mode_on = False
        self._device_handle = SprayMistF638(mac)

    @property
    def device_info(self) -> dict:
        """Generate device info structure

        :return: device info
        :rtype: dict[str, str]
        """
        return {
            "identifiers": {(DOMAIN, self._mac)},
            "name": self._name,
            # "manufacturer": self.light.manufacturername,
            # "model": self.light.productname,
            # "sw_version": self.light.swversion,
            # "via_device": (hue.DOMAIN, self.api.bridgeid),
        }

    def update(self):
        """Updates device, not more frequent than once / minute"""
        _LOGGER.debug("Update called")
        now = datetime.now()
        if now - self._last_update > timedelta(minutes=1):
            self._perform_update()
            self._last_update = now

    def _perform_update(self):
        """Performs actual update of the device data"""
        _LOGGER.debug("..Performing update")
        try:
            connected = False
            for i in range(1, 6):
                connected = self._device_handle.connect()
                if connected:
                    break
                else:
                    _LOGGER.info(
                        "Water timer device: %s not connected retry %d", self._mac, i
                    )
                    sleep(1)
            if connected:
                self._is_available = True
                self._is_running = self._device_handle.running_mode in [
                    RunningMode.RunningAutomatic,
                    RunningMode.RunningManual,
                ]
                self._auto_mode_on = (
                    self._device_handle.working_mode == WorkingMode.Auto
                )
                self._battery_level = int(self._device_handle.battery_level)
            else:
                _LOGGER.warning("Water timer device: %s cannot be reached", self._mac)
                self._is_available = False
        finally:
            self._device_handle.disconnect()

    @property
    def mac(self) -> str:
        """Returns the MAC address

        :return: MAC address of the device
        :rtype: str
        """
        return self._mac

    @property
    def can_connect(self) -> bool:
        """Checks connection to the device

        :return: if connection was successful
        :rtype: bool
        """
        _LOGGER.debug("Reading can_connect")
        return True

    @property
    def is_running(self) -> bool:
        """Checks if the device is active at the moment

        :return: Active state
        :rtype: bool
        """
        _LOGGER.debug("Reading is_running")
        return self._is_running

    @property
    def is_auto_mode_on(self) -> bool:
        """Checks if automated mode is on

        :return: Auto mode state
        :rtype: bool
        """
        _LOGGER.debug("Reading auto_mode")
        return self._auto_mode_on

    @property
    def available(self) -> bool:
        """Reports if the device is connected

        :return: if the device is available
        :rtype: bool
        """
        _LOGGER.debug("Reading availability")
        return self._is_available

    @property
    def battery_level(self) -> Union[int, None]:
        """Reports the device battery level in %

        :return: battery level %
        :rtype: int
        """
        _LOGGER.debug("Reading battery level")
        return self._battery_level
