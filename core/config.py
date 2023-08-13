from django.apps import AppConfig
import signal
import sys
import os

debug = True if os.environ.get("DEBUG") == "True" else False
register = True if os.environ.get("REGISTER") == "True" else False


class InastekConfig(AppConfig):
    """
    InastekConfig Class
    -------------------

    This class represents the configuration for the "core" Django app. It initializes and sets up various configurations when the Django app is ready to be used.

    Attributes:
        name (str): The name of the Django app, which is set to "core" in this case.

    Methods:
        ready(): This method is executed when the Django app is considered ready. It imports the necessary modules, sets up a signal handler to gracefully shut down the app, and starts the scheduler.

    Usage:
        The InastekConfig class is automatically instantiated and executed by Django when the app is initialized. It's used to perform any setup tasks needed for the "core" app.
    """

    name = "core"

    def ready(self):
        from .scheduler import start, stop

        def signal_handler(sig, frame):
            stop()
            sys.exit(0)

        signal.signal(signal.SIGINT, signal_handler)
        start(register)
