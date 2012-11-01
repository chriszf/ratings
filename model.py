from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine, ForeignKey
from sqlalchemy import Column, Integer, String, DateTime, Date

from sqlalchemy.orm import sessionmaker, scoped_session, relationship, backref
import os
import correlation

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
    zipcode = Column(String(15), nullable=True)
    gender = Column(String(1), nullable=True)

    def similarity(self, other):
        u_ratings = {}
        paired_ratings = []
        for r in self.ratings:
            u_ratings[r.movie_id] = r

        for r in other.ratings:
            u_r = u_ratings.get(r.movie_id)
            if u_r:
                paired_ratings.append( (u_r.rating, r.rating) )

        if paired_ratings:
            return correlation.pearson(paired_ratings)
        else:
            return 0.0

    def predict_rating(self, movie):
        if not self.ratings: return None
        ratings = self.ratings
        other_ratings = movie.ratings
        similarities = [ (self.similarity(r.user), r) \
            for r in other_ratings ]
        similarities.sort(reverse = True)
        top = similarities[0]

        similarities = [ sim for sim in similarities if sim[0] > 0 ]
        if not similarities:
            return None
        prediction = sum([ sim * r.rating for sim, r in similarities ])
        denominator = sum( sim[0] for sim in similarities )
        prediction = float(prediction)/denominator
        return prediction


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
    title = Column(String(128), nullable=False)
    released_on = Column(Date, nullable=False)
    imdb_url = Column(String(256))

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
    u1 = session.query(User).get(1)
    m1 = session.query(Movie).get(300)
    main()
