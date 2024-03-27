import mongoengine as me
from app.config import settings


class MongoSession:
    def __init__(self, db, sprocket, factory):
        self.db = db
        self.sprocket = sprocket
        self.factory = factory


def get_db():
    if settings.database_uri:
        db = me.connect(alias=settings.database_name,
                        db=settings.database_name,
                        host=settings.database_uri)

    else:
        db = me.connect(alias=settings.database_name,
                        db=settings.database_name,
                        host='mongodb-dev', port=27017,
                        username=settings.mongodb_root_user,
                        password=settings.mongodb_root_password,
                        authentication_source='admin')
    from app.modules.sprocket.models import Sprocket
    from app.modules.factory.models import Factory
    try:
        session = MongoSession(db, Sprocket, Factory)
        yield session
    finally:
        me.disconnect()
