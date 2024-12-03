from sqlalchemy import Column, Integer, String
from app.database import Base


class Users(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    first_name = Column(String, nullable=False)
    last_name = Column(String, nullable=False)
    age = Column(Integer, nullable=False)
    email = Column(String, unique=True, nullable=False)

    def __repr__(self):
        return f"<User(id={self.id}, first_name={self.first_name}, last_name={self.last_name}, age={self.age}, email={self.email})>"

