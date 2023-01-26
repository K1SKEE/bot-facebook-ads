from sqlalchemy import (
    Column,
    Integer,
    String,
    ForeignKey,
    create_engine,
)
from sqlalchemy.orm import sessionmaker, declarative_base, relationship
from sqlalchemy.exc import IntegrityError

engine = create_engine('sqlite:///db_bot.db', echo=True,
                       pool_recycle=7200)

Base = declarative_base()


class Manager:
    def __init__(self, user_id):
        self.user_id = user_id
        self.session = Session()

    def get_or_create(self, username=None):
        instance = self._retrieve_user()
        if instance:
            return instance
        else:
            instance = self._create_user(username=username)
            return instance

    def _create_user(self, username):
        new_user = User(user_id=self.user_id, username=username)
        self.session.add(new_user)
        self.session.commit()
        return new_user.username

    def _retrieve_user(self):
        user = self.session.query(User).filter_by(user_id=self.user_id).first()
        return user

    def _retrieve_credentials(self):
        pass


class User(Base):
    __tablename__ = 'users'

    user_id = Column(Integer, primary_key=True)
    username = Column(String)

    accounts = relationship('Account', back_populates='user')

    def __repr__(self):
        return f'{self.username}'


class Account(Base):
    __tablename__ = 'accounts'

    id = Column(Integer, primary_key=True)
    username = Column(String)
    password = Column(String)
    proxy = Column(String)
    cookie = Column(String)
    user_id = Column(Integer, ForeignKey("users.user_id"), nullable=False)

    user = relationship('User', back_populates='accounts')

    def __repr__(self):
        return f'{self.username} {self.proxy}'


Base.metadata.create_all(engine)

Session = sessionmaker(bind=engine)
