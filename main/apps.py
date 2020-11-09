from django.apps import AppConfig
#from signals import my_callback

class MainConfig(AppConfig):
    name = 'main'
    def ready(self):
        import main.signals

