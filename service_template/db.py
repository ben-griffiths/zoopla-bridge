from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class User(db.Model):
    """Data model for users"""

    __tablename__ = "users"

    id = db.Column(
        db.Integer,
        primary_key=True,
    )
    created = db.Column(db.DateTime, index=False, unique=False, nullable=False)

    def __repr__(self):
        return "<User {}>".format(self.id)
