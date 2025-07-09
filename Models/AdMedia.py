from Config.db import Base
from sqlalchemy import Column, Integer, String


class AdMedia(Base):
    __tablename__ = 'tbl_ad_media'

    id = Column(Integer, primary_key=True, autoincrement=True, nullable=False)

    ad_id = Column(Integer)

    screen_resolution_width = Column(Integer)
    screen_resolution_height = Column(Integer)

    media_url = Column(String(255)) 
