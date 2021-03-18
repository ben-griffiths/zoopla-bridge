from sqlalchemy import select
from sqlalchemy.exc import OperationalError

from service_template import models


def can_select(conn):
    s = select(models.User)
    try:
        conn.execute(s)
    except OperationalError:
        return False
    return True
