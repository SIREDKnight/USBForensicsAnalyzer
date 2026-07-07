from abc import ABC, abstractmethod


class BaseCollector(ABC):
    """
    Abstract base class for all forensic artifact collectors.

    Every collector must implement the collect()
    method and return collected forensic artifacts.
    """


    def __init__(self):
        """
        Common initialization point for collectors.
        Future collectors can inherit configuration,
        logging, or hashing here.
        """
        pass


    @abstractmethod
    def collect(self):
        """
        Collect forensic artifacts.

        Returns:
            list:
                A list containing collected artifacts.
        """
        pass