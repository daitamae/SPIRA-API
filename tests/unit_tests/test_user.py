from fastapi.testclient import TestClient
from src.app import create_app


from tests.unit_tests.test_configuration import inject_dependencies
from tests.mocks.mongo_mock import MongoMock
from src.domain.ports.database_port import DatabasePort


def plug_adapters_to_ports():
    ports = {}
    ports["database"] = DatabasePort(MongoMock())
    return ports


ports = plug_adapters_to_ports()
app = create_app(ports["database"])
client = TestClient(app)


def test_get_user_by_id_success():
    response = client.get("/v1/users/507f1f77bcf86cd799439011")
    assert response.status_code == 200
    assert response.json() == {
        "id": "507f1f77bcf86cd799439011",
        "email": "test_email",
        "username": "test_username",
    }


def test_get_user_by_id_invalid_id_exception():
    response = client.get("/v1/users/invalid_id")
    assert response.status_code == 400
    assert response.json() == {"detail": "user id is not valid"}


def test_get_user_by_id_not_found_exception():
    response = client.get("/v1/users/507f1f77bcf86cd799439021")
    assert response.status_code == 404
    assert response.json() == {"detail": "user not found"}
