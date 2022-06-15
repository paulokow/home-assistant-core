try:
    from bluepy import btle
except ImportError:
    pass

from datetime import datetime, timedelta
import logging
from random import randint

_LOGGER = logging.getLogger(__name__)


class WaterTimerDevice:
    """AI is creating summary for"""

    def __init__(self, mac: str) -> None:
        self._mac = mac
        self._last_update = datetime.min
        self._is_running = False
        self._auto_mode_on = False

    def update(self):
        """Updates device, not more frequent than once / minute"""
        now = datetime.now()
        if now - self._last_update > timedelta(minutes=1):
            self._perform_update()
            self._last_update = now

    def _perform_update(self):
        """Performs actual update of the device data"""
        _LOGGER.info("Performing update")
        self._is_running = randint(0, 1) == 1
        self._auto_mode_on = randint(0, 1) == 1

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
        _LOGGER.info("Reading can_connect")
        return True

    @property
    def is_running(self) -> bool:
        """Checks if the device is active at the moment

        :return: Active state
        :rtype: bool
        """
        _LOGGER.info("Reading is_running")
        return self._is_running

    @property
    def is_auto_mode_on(self) -> bool:
        """Checks if automated mode is on

        :return: Auto mode state
        :rtype: bool
        """
        _LOGGER.info("Reading auto_mode")
        return self._auto_mode_on
