from typing import Optional
from fastapi import FastAPI, Depends
from sqlalchemy import text, bindparam
from sqlalchemy.orm import Session
from .database import SessionLocal
import datetime

app = FastAPI()


# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.get("/data")
def data(date: datetime.date, publishers: Optional[str] = None, titles: Optional[str] = None,
         country_codes: Optional[str] = None, db: Session = Depends(get_db)):
    params = {
        'date': str(date),
    }

    if titles:
        titles = [title for title in titles.split(',')]
        where_clause_titles = 'thismonth.title IN :titles'
        params['titles'] = titles
    else:
        where_clause_titles = '1'

    if country_codes:
        country_codes = [country_code for country_code in country_codes.split(',')]
        where_clause_country_codes = 'thismonth.country_code IN :country_codes'
        params['country_codes'] = country_codes
    else:
        where_clause_country_codes = '1'

    if publishers:
        publishers = [publisher for publisher in publishers.split(',')]
        where_clause_publishers = 'dimensions.publisher IN :publishers'
        params['publishers'] = publishers
    else:
        where_clause_publishers = '1'

    # Raw SQL because its easier for me and I don't have much time left.
    # But using the ORM would be a lot cleaner.
    sql_tmp = """
    SELECT thismonth.date AS date, thismonth.title, dimensions.publisher, dimensions.main_genre, 
        SUM(thismonth.players) AS players, (SUM(thismonth.players) - SUM(lastmonth.players)) AS player_growth
    FROM game_facts AS thismonth
    JOIN game_dimensions AS dimensions
    ON thismonth.atlas_id = dimensions.game_id
    LEFT JOIN game_facts AS lastmonth
    ON thismonth.date = Date(lastmonth.date, '+1 months')
    AND thismonth.title = lastmonth.title
    AND thismonth.device = lastmonth.device
    AND thismonth.platform = lastmonth.platform
    AND thismonth.country_code = lastmonth.country_code
    AND thismonth.atlas_id = lastmonth.atlas_id
    WHERE thismonth.date = :date 
    AND """ + where_clause_titles + """
    AND """ + where_clause_publishers + """
    AND """ + where_clause_country_codes + """
    GROUP BY thismonth.title
    """

    t = text(sql_tmp)
    if publishers:
        t = t.bindparams(bindparam('publishers', expanding=True))
    if country_codes:
        t = t.bindparams(bindparam('country_codes', expanding=True))
    if titles:
        t = t.bindparams(bindparam('titles', expanding=True))

    return [metric for metric in db.execute(t, params)]
