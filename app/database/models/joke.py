from datetime import datetime
from email.policy import default
from typing import Optional

from sqlalchemy import (
    Column,
    Integer,
    String,
)

from app.database import session
from app.database.models.base import Base


class Joke(Base):
    __tablename__ = "jokes"

    number = Column(Integer, primary_key=True, autoincrement=True)
    text = Column(String, nullable=False)
    created_at = Column(String, nullable=False)
    updated_at = Column(String, nullable=False, default=datetime.utcnow, onupdate=datetime.utcnow)
    deleted_at = Column(String, nullable=True, default=None)

    def save(self) -> "Joke":
        session.add(self)
        session.commit()
        return self

    @classmethod
    def get_by_number(cls, number: int) -> Optional["Joke"]:
        return session.query(Joke).get(number)

    def update(self, text: str) -> "Joke":
        self.text = text
        session.add(self)
        session.commit()
        return self

    def delete(self) -> "Joke":
        self.deleted_at = datetime.utcnow()
        session.add(self)
        session.commit()
        return self
