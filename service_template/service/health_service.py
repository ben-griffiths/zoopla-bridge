from service_template.repository.health_repo import can_select


class HealthService:
    def __init__(self, db_engine) -> None:
        self.db_engine = db_engine

    def get_health(self):
        with self.db_engine.begin() as conn:
            db_health = can_select(conn)
        return {"ok": True, "db": db_health}
