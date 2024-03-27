import mongomock
import pytest
import mongoengine as me
from mongoengine.context_managers import switch_db
from fastapi.testclient import TestClient
from app.main import app
from app.config import settings
from app.database import get_db, MongoSession
from app.core.schemas import ResponseStatus
from app.modules.sprocket.schemas import RegisterSprocketRequest
from app.modules.sprocket.service import register_sprocket
from app.modules.factory.schemas import RegisterFactoryRequest
from app.modules.factory.service import register_factory
from app.modules.sprocket.models import Sprocket
from app.modules.factory.models import Factory


@pytest.fixture
def session():
    db = me.connect(alias='test',
                    db='powerflex-demo-tst',
                    host='mongodb://localhost',
                    mongo_client_class=mongomock.MongoClient)
    session = MongoSession(db, None, None)
    try:
        if settings.database_uri:
            me.register_connection(alias=settings.database_name,
                                   db=settings.database_name,
                                   host=settings.database_uri)

        else:
            me.register_connection(alias=settings.database_name,
                                   db=settings.database_name,
                                   host='mongodb-dev', port=27017,
                                   username=settings.mongodb_root_user,
                                   password=settings.mongodb_root_password,
                                   authentication_source='admin')
        session.sprocket = switch_db(Sprocket, 'test').__enter__()
        session.factory = switch_db(Factory, 'test').__enter__()
        yield session
    finally:
        me.register_connection(alias='test',
                               db='powerflex-demo-tst',
                               host='mongodb://localhost',
                               mongo_client_class=mongomock.MongoClient)
        session.sprocket = switch_db(Sprocket, settings.database_name).__enter__()
        session.factory = switch_db(Factory, settings.database_name).__enter__()
        me.disconnect(alias='test')


@pytest.fixture
def client(session):
    def override_get_db():
        try:
            yield session
        finally:
            me.disconnect('test')
    app.dependency_overrides[get_db] = override_get_db
    yield TestClient(app)


@pytest.fixture
def authorized_client(client):
    client.headers = {
        **client.headers,
        "api_key": settings.api_key
    }
    return client


def test_root(client):
    res = client.get('/')
    assert res.json()['ok']
    assert res.status_code == 200


@pytest.fixture
def test_sprocket(client, session):
    sprocket_data = RegisterSprocketRequest(
        teeth=5,
        pitch_diameter=5,
        outside_diameter=6,
        pitch=1
    )
    register_sprocket_response = register_sprocket(session.sprocket, sprocket_data)
    assert register_sprocket_response.status == ResponseStatus.OK
    return register_sprocket_response.data


@pytest.fixture
def test_sprockets(client, session):
    sprocket_data = [RegisterSprocketRequest(
        teeth=x+4,
        pitch_diameter=x+4,
        outside_diameter=x+5,
        pitch=x
    ) for x in range(5, 8)]
    register_sprocket_response = [register_sprocket(session.sprocket, sp).data for sp in sprocket_data]
    return register_sprocket_response


@pytest.fixture
def test_factory(session):
    factory_data = RegisterFactoryRequest.model_validate({"factory": {
                                                            "chart_data": {
                                                              "sprocket_production_actual": [
                                                                32,
                                                                29,
                                                                31,
                                                                30
                                                              ],
                                                              "sprocket_production_goal": [
                                                                32,
                                                                30,
                                                                31,
                                                                29
                                                              ],
                                                              "time": [
                                                                1611194818,
                                                                1611194878,
                                                                1611194938,
                                                                1611194998
                                                              ]
                                                             }
                                                            }
                                                          })

    register_factory_response = register_factory(session.factory, factory_data)
    assert register_factory_response.status == ResponseStatus.OK
    return register_factory_response.data


@pytest.fixture
def test_factories(session):
    factory_data = [RegisterFactoryRequest.model_validate({"factory": {
                                                            "chart_data": {
                                                              "sprocket_production_actual": [
                                                                x + 32,
                                                                x + 29,
                                                                x + 31
                                                              ],
                                                              "sprocket_production_goal": [
                                                                x + 32,
                                                                x + 30,
                                                                x + 31
                                                              ],
                                                              "time": [
                                                                x + 1611194818,
                                                                x + 1611194878,
                                                                x + 1611194938
                                                              ]
                                                             }
                                                            }
                                                           }) for x in range(1, 4)]

    register_factory_response = [register_factory(session.factory, fc).data for fc in factory_data]
    return register_factory_response
