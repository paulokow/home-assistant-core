try:
    from bluepy import btle
except ImportError:
    pass

import logging
from random import randint

_LOGGER = logging.getLogger(__name__)


class WaterTimerDevice:
    def __init__(self, mac: str):
        self._mac = mac

    @property
    def mac(self):
        return self._mac

    @property
    def can_connect(self):
        _LOGGER.info("reading can_connect")
        return True

    @property
    def is_running(self):
        _LOGGER.info("reading is_running")
        return randint(0, 1) == 1

    @property
    def is_auto_mode_on(self):
        _LOGGER.info("reading auto_mode")
        return randint(0, 1) == 1
