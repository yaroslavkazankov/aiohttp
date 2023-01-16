# import asyncio
import sqlalchemy as db
from sqlalchemy.orm import declarative_base
from settings import URI

Base = declarative_base()


class Users(Base):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    mail = db.Column(db.String(100), nullable=False)
    password = db.Column(db.Text(), nullable=False)

    def __init__(self, name="default", mail="default", password="default"):
        self.name = name
        self.mail = mail
        self.password = password

    def __repr__(self):
        return f"Name: {self.name}"

    def to_dict(self):
        return {'id': self.id,
                'name': self.name,
                'mail': self.mail
                }


class Notifications(Base):
    __tablename__ = 'notifications'

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255), nullable=False)
    description = db.Column(db.Text, nullable=False)
    date = db.Column(db.String(255), nullable=False)
    owner_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)

    def __init__(self, title="default",
                 description="default",
                 date="default",
                 owner_id=0
                 ):
        self.title = title
        self.description = description
        self.date = date
        self.owner_id = owner_id

    def __repr__(self):
        return (f"'id': {self.id}, 'title': {self.title}, 'description':"
                f" {self.description}, 'date': {self.date},"
                f" 'owner_id': {self.owner_id}"
                )


    def to_dict(self):
        return {'id': self.id,
                'title': self.title,
                'description': self.description,
                'date': self.date,
                'owner id': self.owner_id
                }


if __name__ == "__main__":
    engine = db.create_engine(URI)
    Base.metadata.create_all(engine,
                             Base.metadata.tables.values(),
                             checkfirst=True
                             )