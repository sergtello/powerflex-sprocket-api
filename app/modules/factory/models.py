import mongoengine as me
from app.config import settings
from mongoengine.errors import ValidationError
from datetime import datetime


class ChartData(me.EmbeddedDocument):
    sprocket_production_actual = me.ListField(
        field=me.IntField(min_value=0),
        db_field='sprocketProductionActual',
        required=True)
    sprocket_production_goal = me.ListField(
        field=me.IntField(min_value=0),
        db_field='sprocketProductionGoal',
        required=True)
    time = me.ListField(field=me.DateTimeField(), required=True)


class FactoryChartData(me.EmbeddedDocument):
    chart_data = me.EmbeddedDocumentField(ChartData, db_field='chartData', required=True)

    def clean(self):
        if not (len(self.chart_data['sprocket_production_actual'])
                == len(self.chart_data['sprocket_production_goal'])
                == len(self.chart_data['time'])):
            raise ValidationError("Sprocket's factory chart data must contain arrays of the same length")


class Factory(me.Document):
    factory = me.EmbeddedDocumentField(FactoryChartData, required=True)

    creation_time = me.DateTimeField(db_field="creationTime")
    modified_time = me.DateTimeField(default=datetime.now, db_field="modifiedTime")

    def save(self, *args, **kwargs):
        if not self.creation_time:
            self.creation_time = datetime.utcnow()
        self.modified_time = datetime.utcnow()
        return super(Factory, self).save(*args, **kwargs)

    meta = {
        'db_alias': settings.database_name,
        'collections': 'factories'
    }
