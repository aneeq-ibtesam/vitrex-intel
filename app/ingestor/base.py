from abc import ABC, abstractmethod

class BaseIngestor(ABC):
    @abstractmethod
    def ingest(self):
        """
        Fetch data and return a list of STIX 2.1 dicts.
        """
        pass
