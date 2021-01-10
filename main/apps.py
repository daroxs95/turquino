from django.apps import AppConfig
#from signals import my_callback

class MainConfig(AppConfig):
    name = 'main'
    #def ready(self): #this will set signals containing the reset cache
    #    import main.signals

