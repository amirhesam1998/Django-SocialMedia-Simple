from django.apps import AppConfig


class AccountConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "account"
    
    def ready(self):
        '''
        Apply the written signal file to the entire application
        '''
        from . import signals
