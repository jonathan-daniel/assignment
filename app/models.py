from sqlalchemy import Column, ForeignKey, Date, Integer, String
from sqlalchemy.orm import relationship

from .database import Base


class GameFacts(Base):
    __tablename__ = 'game_facts'

    date = Column(Date, primary_key=True)
    platform = Column(String, primary_key=True)
    country_code = Column(String, primary_key=True)
    market_name = Column(String)
    region_name = Column(String)
    title = Column(String, primary_key=True)
    device = Column(String, primary_key=True)
    atlas_id = Column(String, ForeignKey('game_dimensions.game_id'), primary_key=True)
    atlas = relationship("GameDimensions")
    players = Column(Integer)


class GameDimensions(Base):
    __tablename__ = 'game_dimensions'

    game_name = Column(String)
    game_id = Column(String, primary_key=True)
    main_genre = Column(String)
    main_theme = Column(String)
    publisher = Column(String)
