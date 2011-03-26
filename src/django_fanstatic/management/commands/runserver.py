from optparse import make_option

from django.conf import settings
from django.core.management.commands.runserver import BaseRunserverCommand

from fanstatic.wsgi import Fanstatic

class Command(BaseRunserverCommand):
    help = "Starts a django development webserver that uses the fanstatic WSGI middleware."

    def get_handler(self, *args, **options):
        """
        Returns the Fanstatic serving handler.
        """
        application = super(Command, self).get_handler(*args, **options)
        wrapped_application = Fanstatic(application, base_url='')

        return wrapped_application
