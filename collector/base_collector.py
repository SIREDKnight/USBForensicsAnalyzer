from abc import ABC, abstractmethod


class BaseCollector(ABC):
    """
    Base class for all forensic collectors.
    Every collector must implement collect().
    """

    @abstractmethod
    def collect(self):
        """Collect forensic artifacts."""
        pass