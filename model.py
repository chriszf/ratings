from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine, ForeignKey
from sqlalchemy import Column, Integer, String, DateTime, Date

from sqlalchemy.orm import sessionmaker, scoped_session, relationship, backref
import os

db_uri = os.environ.get("DATABASE_URL", "sqlite:///ratings.db")
    
engine = create_engine(db_uri, echo=False) 
session = scoped_session(sessionmaker(bind=engine,
                         autocommit = False,
                         autoflush = False))

Base = declarative_base()
Base.query = session.query_property

### Class declarations go here

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key = True)
    email = Column(String(64), nullable=True)
    password = Column(String(64), nullable=True)        
    age = Column(Integer, nullable=True)
    zipcode = Column(Integer, nullable=True)
    gender = Column(String(1), nullable=True)

class Rating(Base):
    __tablename__ = "ratings"

    id = Column(Integer, primary_key = True)
    user_id = Column(Integer, ForeignKey('users.id'))
    movie_id = Column(Integer, ForeignKey('movies.id'))
    rating = Column(Integer, nullable=False)

    user = relationship("User", backref="ratings")
    movie = relationship("Movie", backref="ratings")

class Movie(Base):
    __tablename__ = "movies"
    id = Column(Integer, primary_key = True)
    title = Column(String(64), nullable=False)
    released_on = Column(Date, nullable=False)
    imdb_url = Column(String(128))

### End class declarations

def create_db():
    Base.metadata.create_all(engine)

def connect(db_uri="sqlite:///ratings.db"):
    global engine
    global session
    engine = create_engine(db_uri, echo=False) 
    session = scoped_session(sessionmaker(bind=engine,
                             autocommit = False,
                             autoflush = False))

def main():
    """In case we need this for something"""
    pass

if __name__ == "__main__":
    main()
