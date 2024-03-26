import mongoengine as me
from app.config import settings
from datetime import datetime


class Sprocket(me.Document):
    teeth = me.IntField(required=True, min_value=1)
    pitch_diameter = me.IntField(db_field='pitchDiameter', required=True, min_value=1)
    outside_diameter = me.IntField(db_field='outsideDiameter', required=True, min_value=1)
    pitch = me.IntField(required=True, min_value=1)

    creation_time = me.DateTimeField(db_field="creationTime")
    modified_time = me.DateTimeField(default=datetime.now, db_field="modifiedTime")

    def save(self, *args, **kwargs):
        if not self.creation_time:
            self.creation_time = datetime.utcnow()
        self.modified_time = datetime.utcnow()
        return super(Sprocket, self).save(*args, **kwargs)

    meta = {
        'db_alias': settings.database_name,
        'collections': 'sprockets'
    }

