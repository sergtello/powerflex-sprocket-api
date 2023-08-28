import mongoengine as me
from app.config import settings

db = me.connect(alias=settings.database_alias, db=settings.database_name, host=settings.database_uri)
