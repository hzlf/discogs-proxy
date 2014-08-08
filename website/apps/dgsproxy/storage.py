import logging

from django.core.files.storage import FileSystemStorage

log = logging.getLogger(__name__)

class ReplaceFileStorage(FileSystemStorage):
    """
    Custom FileSystemStorage:
    Instead of the default behavior (adding a number to the filename) this one replaces existing files.
    """
    def get_available_name(self, name):
        self.delete(name)
        return name

