from django.apps import AppConfig


class CoreConfig(AppConfig):
    name = 'core'

    def ready(self):
        print('core apps is ready')
        from actstream import registry
        registry.register(self.get_model('Document'))
