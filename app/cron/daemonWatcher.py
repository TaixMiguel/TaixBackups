#!/usr/bin/python3

import logging
import threading
import time

import app.toolInit

logger = logging.getLogger(__name__)


class DaemonWatcher:

    turnOff: bool
    timeSleep: int

    def __init__(self) -> None:
        # TODO: cambiar a un minuto cuando toque mirar en BBDD
        self.timeSleep = 30 * 60  # Cada 30 minutos (se mide en segundos)

    def run(self) -> None:
        thread = threading.Thread(target=self.__turn_on, name='DaemonWatcher')
        thread.start()

    def __turn_on(self) -> None:
        logger.debug('Inicio de DaemonWatcher')
        self.turnOff = False

        while not self.turnOff:
            logger.debug('Nueva iteración')
            result = int(time.strftime("%H%M", time.localtime()))

            if 0 < result < 30:  # Se lanza entre las 00:00 y las 00:30
                app.toolInit.servicios_mqtt()
            time.sleep(self.timeSleep)

    def turn_off(self) -> None:
        self.turnOff = True
