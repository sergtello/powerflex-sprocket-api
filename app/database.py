import mongoengine as me
from app.config import settings

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
