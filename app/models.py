import mongoengine as me
from app.config import settings
from mongoengine.errors import ValidationError


class Sprocket(me.Document):
    teeth = me.IntField(required=True, min_value=1)
    pitch_diameter = me.IntField(db_field='pitchDiameter', required=True, min_value=1)
    outside_diameter = me.IntField(db_field='outsideDiameter', required=True, min_value=1)
    pitch = me.IntField(required=True, min_value=1)

    meta = {
        'db_alias': settings.database_alias,
        'collections': 'sprockets'
    }


class ChartData(me.EmbeddedDocument):
    sprocket_production_actual = me.ListField(field=me.IntField(min_value=0), db_field='sprocketProductionActual', required=True)
    sprocket_production_goal = me.ListField(field=me.IntField(min_value=0), db_field='sprocketProductionGoal', required=True)
    time = me.ListField(field=me.DateTimeField(), required=True)


class FactoryChartData(me.EmbeddedDocument):
    chart_data = me.EmbeddedDocumentField(ChartData, db_field='chartData', required=True)


class Factory(me.Document):
    factory = me.EmbeddedDocumentField(FactoryChartData, required=True)

    def save(self, *args, **kwargs):
        if not (len(self.factory['chart_data']['sprocket_production_actual'])
                == len(self.factory['chart_data']['sprocket_production_goal'])
                == len(self.factory['chart_data']['time'])):
            raise ValidationError("Sprocket's factory chart data must contain arrays of the same length")
        return super(Factory, self).save(*args, **kwargs)

    meta = {
        'db_alias': settings.database_alias,
        'collections': 'factories'
    }
