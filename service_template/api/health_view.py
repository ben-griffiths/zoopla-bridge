class HealthView:
    def __init__(self, health_service) -> None:
        self.health_service = health_service

    def get_health(self):
        return self.health_service.get_health()
