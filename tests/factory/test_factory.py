from fastapi import status
from app.core.schemas import ResponseStatus
from app.modules.factory import schemas as sch
from bson.objectid import ObjectId


def test_get_all_factories(client, test_factories):
    res = client.get('/v1/factories')
    factories = res.json()['data']
    assert res.json()['status'] == ResponseStatus.OK
    assert len(factories) == len(test_factories)
    assert res.status_code == 200


def test_get_factory_by_id(client, test_factory):
    res = client.get(f'/v1/factories/{test_factory.id}')
    factory = sch.GetFactoryResponse.model_validate(res.json())
    assert factory.status == ResponseStatus.OK
    assert factory.data.id == test_factory.id
    assert factory.data.factory.chart_data.sprocket_production_actual == test_factory.factory.chart_data.sprocket_production_actual
    assert factory.data.factory.chart_data.sprocket_production_goal == test_factory.factory.chart_data.sprocket_production_goal
    assert res.status_code == status.HTTP_200_OK


def test_register_factory(authorized_client):
    time_arr = [1611194818, 1611194878, 1611194938, 1611194998, 1611195058]
    chart = sch.ChartDataBase(
        sprocket_production_actual=[32, 29, 31, 30, 32],
        sprocket_production_goal=[32, 30, 31, 29, 32],
        time=time_arr
    )
    res = authorized_client.post('/v1/factories', json={
        "factory": {
            "chart_data": chart.model_dump(exclude={'time'}) | {'time': time_arr}
        }
    })
    register_factory_response = sch.RegisterFactoryResponse.model_validate(res.json())
    new_factory = register_factory_response.data

    assert res.status_code == status.HTTP_201_CREATED
    assert register_factory_response.status == ResponseStatus.OK
    for key in chart.model_dump(exclude_none=True, exclude_unset=True).keys():
        assert getattr(new_factory.factory.chart_data, key) == getattr(chart, key)
    assert type(new_factory.id) is ObjectId


def test_unauthorized_register_factory(client):
    res = client.post('/v1/factories', json={
        "factory": {
            "chart_data": {
                "sprocket_production_actual": [],
                "sprocket_production_goal": [],
                "time": []
            }
        }
    })
    assert res.status_code == status.HTTP_403_FORBIDDEN


def test_upload_factory_data_file(authorized_client):
    res = authorized_client.post('/v1/factories/upload',
                                 files={'document': open('sample/seed_factory_data.json', 'rb')})
    assert res.status_code == status.HTTP_201_CREATED
    assert res.json()['status'] == ResponseStatus.OK
