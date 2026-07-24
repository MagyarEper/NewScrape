from abc import ABC, abstractmethod


class NewsSource(ABC):

    @abstractmethod
    def fetch(self):
        """
        Returns a list of dictionaries.

        Later every fetcher
        (Telex, HVG, Index...)
        will implement this method.
        """
        pass