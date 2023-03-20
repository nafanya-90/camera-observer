from abc import ABC, abstractmethod

class AbstractUploadService(ABC):
    """Abstract service to upload files somewhere"""

    @abstractmethod
    def upload(self, filepath):
        pass
