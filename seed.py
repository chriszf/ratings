import model
import csv
import sqlalchemy.exc
import datetime
import re

def load_users(session):
    with open("seed_data/u.user") as f:
        reader = csv.reader(f, delimiter="|")
        for row in reader:
            id, age, gender, occupation, zipcode = row
            id = int(id)
            age = int(age)
            u = model.User(id=id, age=age, email=None, password=None, zipcode=zipcode, gender=gender)
            session.add(u)
        try:
            session.commit()
        except sqlalchemy.exc.IntegrityError, e:
            session.rollback()

def load_movies(session):
    # use u.item
    with open("seed_data/u.item") as f:
        reader = csv.reader(f, delimiter="|")
        for row in reader:
            id = int(row[0])
            title = row[1].decode("latin_1")
            title = re.sub("\(\d{4}\)", "", title)
            url = row[4]
            release_date = row[2]
            if not release_date:
                continue
            release_date = datetime.datetime.strptime(release_date, "%d-%b-%Y")

            m = model.Movie(id=id, title=title, released_on=release_date, imdb_url=url)
            session.add(m)
        
        try:
            session.commit()
        except:
            session.rollback()

def load_ratings(session):
    # use u.data
    with open("seed_data/u.data") as f:
        reader = csv.reader(f, delimiter="\t")
        for row in reader:
            user_id = int(row[0])
            movie_id = int(row[1])
            rating = int(row[2])
            
            r = model.Rating(user_id=user_id, movie_id=movie_id, rating=rating)
            session.add(r)
        session.commit()

def main(session):
    # You'll call each of the load_* functions with the session as an argument
    load_users(session)
    load_movies(session)
    load_ratings(session)

if __name__ == "__main__":
    s = model.session
    main(s)
