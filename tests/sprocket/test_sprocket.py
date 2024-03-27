from fastapi import status
from app.core.schemas import ResponseStatus
from app.modules.sprocket import schemas as sch
from bson.objectid import ObjectId


def test_get_all_sprockets(client, test_sprockets):
    res = client.get('/v1/sprockets')
    sprockets = res.json()['data']
    assert res.json()['status'] == ResponseStatus.OK
    assert len(sprockets) == len(test_sprockets)
    assert res.status_code == 200


def test_get_sprocket_by_id(client, test_sprocket):
    res = client.get(f'/v1/sprockets/{test_sprocket.id}')
    sprocket = sch.GetSprocketResponse.model_validate(res.json())
    assert sprocket.status == ResponseStatus.OK
    assert sprocket.data.id == test_sprocket.id
    for field in sch.SprocketBase.model_fields:
        assert getattr(sprocket.data, field) == getattr(test_sprocket, field)
    assert res.status_code == status.HTTP_200_OK


def test_register_sprocket(authorized_client):
    sprocket = sch.RegisterSprocketRequest(
        teeth=6,
        pitch_diameter=6,
        outside_diameter=7,
        pitch=1
    )
    res = authorized_client.post('/v1/sprockets', json=sprocket.model_dump())
    register_sprocket_response = sch.RegisterSprocketResponse.model_validate(res.json())
    new_sprocket = register_sprocket_response.data

    assert res.status_code == status.HTTP_201_CREATED
    assert register_sprocket_response.status == ResponseStatus.OK
    for key in sprocket.model_dump(exclude_none=True, exclude_unset=True).keys():
        assert getattr(new_sprocket, key) == getattr(sprocket, key)
    assert type(new_sprocket.id) is ObjectId


def test_unauthorized_register_sprocket(client):
    res = client.post('/v1/sprockets', json={
        'teeth': 1,
        'pitch_diameter': 1,
        'outside_diameter': 1,
        'pitch': 1
    })
    assert res.status_code == status.HTTP_403_FORBIDDEN


def test_update_sprocket(authorized_client, test_sprocket):
    updated_fields = sch.UpdateSprocketRequest(
        teeth=12,
        pitch=3
    )
    res = authorized_client.patch(f'/v1/sprockets/{test_sprocket.id}', json=updated_fields.model_dump(exclude_none=True, exclude_unset=True))
    update_sprocket_response = sch.UpdateSprocketResponse.model_validate(res.json())
    updated_sprocket = update_sprocket_response.data
    assert res.status_code == status.HTTP_200_OK
    assert update_sprocket_response.status == ResponseStatus.OK
    for key in updated_fields.model_dump(exclude_none=True, exclude_unset=True).keys():
        assert getattr(updated_sprocket, key) == getattr(updated_fields, key)


def test_upload_sprocket_file(authorized_client):
    res = authorized_client.post('/v1/sprockets/upload',
                                 files={'document': open('sample/seed_sprocket_types.json', 'rb')})
    assert res.status_code == status.HTTP_201_CREATED
    assert res.json()['status'] == ResponseStatus.OK
