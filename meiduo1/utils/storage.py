from django.core.files.storage import Storage
from django.conf import settings

class MyStorage(Storage):
    def _open(self,name, mode='rb'):
        pass
    def _save(self,name, content, max_length=None):
        pass
    def url(self, name):
        return "http://192.168.36.34:8888/" + name