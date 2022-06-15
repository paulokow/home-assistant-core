try:
    from bluepy import btle
except ImportError:
    pass

import logging
from random import randint

_LOGGER = logging.getLogger(__name__)


class WaterTimerDevice:
    """AI is creating summary for"""

    def __init__(self, mac: str) -> None:
        self._mac = mac

    @property
    def mac(self):
        return self._mac

    @property
    def can_connect(self):
        _LOGGER.info("Reading can_connect")
        return True

    @property
    def is_running(self):
        _LOGGER.info("Reading is_running")
        return randint(0, 1) == 1

    @property
    def is_auto_mode_on(self):
        _LOGGER.info("Reading auto_mode")
        return randint(0, 1) == 1
