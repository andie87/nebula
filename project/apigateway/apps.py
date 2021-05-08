from django.apps import AppConfig

class RestApiGatewayConfig(AppConfig):
    name = 'apigateway'

    def ready(self):
        import apigateway.signals

