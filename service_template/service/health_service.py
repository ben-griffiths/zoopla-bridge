from service_template.db import User


class HealthService:
    def __init__(self) -> None:
        pass

    def get_health(self):
        db_health = True
        try:
            User.query.all()
        except Exception:
            db_health = False
        return {"ok": True, "db": db_health}
