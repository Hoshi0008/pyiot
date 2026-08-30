# -*- coding: utf-8 -*-
from abc import ABC, abstractmethod


class Transport(ABC):
    @abstractmethod
    def open(self) -> None:
        """Open a connection, or throw an exception."""
        pass

    @abstractmethod
    def close(self) -> None:
        """Close the connection."""
        pass

    @property
    @abstractmethod
    def is_open(self) -> bool:
        """Return True if a connection has opened, or False."""
        pass

    @abstractmethod
    def read(self, nbytes: int, timeout: float | None = None) -> bytes:
        """
        Read nbytes at most in UartTransport.
        I2C/SPI return exactly nbytes.
        Return the part that has been read when timeout.
        """
        pass

    @abstractmethod
    def write(self, data: bytes) -> int:
        """Send the origin bytes, return the size of data that has been exactly written."""
        pass

    def transfer(self, data: bytes) -> bytes:
        raise NotImplementedError("This transport layer doesn't support this method!")

    def flush(self) -> None:
        """Clear the input and output buffer."""
        pass

    def wait(self) -> None:
        """Waiting for the data until finish writing."""
        raise NotImplementedError("This transport layer doesn't support this method!")

    def __enter__(self) -> "Transport":
        self.open()
        return self

    def __exit__(self, *exc) -> None:
        self.close()
