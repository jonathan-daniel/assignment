# I used this script to seed the database, but the database is already included as a file.

import csv
import datetime

from app import models
from app.database import SessionLocal, engine, Base

db = SessionLocal()

# drop all tables
Base.metadata.drop_all(bind=engine)

# create all tables
Base.metadata.create_all(bind=engine)

with open('data/game_dimensions.csv', 'r') as f:
    csv_reader = csv.DictReader(f)
    for row in csv_reader:
        db_record = models.GameDimensions(
            game_name=row['game_name'],
            game_id=row['game_id'],
            main_genre=row['main_genre'],
            main_theme=row['main_theme'],
            publisher=row['publisher']
        )
        db.add(db_record)

    db.commit()

with open('data/game_facts.csv', 'r') as f:
    csv_reader = csv.DictReader(f)
    for row in csv_reader:
        db_record = models.GameFacts(
            date=datetime.datetime.strptime(row['date'], '%Y-%m-%d'),
            platform=row['platform'],
            country_code=row['country_code'],
            market_name=row['market_name'],
            region_name=row['region_name'],
            title=row['title'],
            device=row['device'],
            atlas_id=row['atlas_id'],
            players=int(row['players'])
        )
        db.add(db_record)

    db.commit()
db.close()
