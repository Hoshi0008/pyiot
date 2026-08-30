# -*- coding: utf-8 -*-
from . import Transport
import serial


class UartTransport(Transport):
    def __init__(self, **kwargs):
        self.serial = serial.Serial(**kwargs)

    @property
    def is_open(self) -> bool:
        return self.serial.is_open

    def open(self) -> None:
        self.serial.open()

    def close(self) -> None:
        self.serial.close()

    def read(self, nbytes: int, timeout: float | None = None) -> bytes:
        if timeout is not None:
            old = self.serial.timeout
            self.serial.timeout = timeout
            data = self.serial.read(nbytes)
            self.serial.timeout = old
        else:
            data = self.serial.read(nbytes)
        return data

    def write(self, data: bytes) -> int:
        return self.serial.write(data)

    def flush(self) -> None:
        self.serial.reset_output_buffer()
        self.serial.reset_input_buffer()

    def wait(self) -> None:
        self.serial.flush()
