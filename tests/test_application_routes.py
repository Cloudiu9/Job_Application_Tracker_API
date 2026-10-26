import pytest
from app import app as flask_app 

NON_EXISTENT_ID = 9999999999

@pytest.fixture
def client(monkeypatch):
    monkeypatch.setitem(flask_app.config, "TESTING", True)

    with flask_app.test_client() as client:
        yield client

@pytest.fixture
def existing_application(client):
    """Creates an application for the current test; the database transaction is rolled back during teardown."""
    payload = {
        "company": "Bosch", 
        "title": "Junior Engineer", 
        "status" : "applied", 
        "date_applied": '2026-10-26'
    }
    response = client.post("/applications", json=payload)

    assert response.status_code == 201
    return response

def test_get_all_applications_success(client, existing_application):
    payload2 = {
        "company": "Kaufland",
        "title": "Senior Engineer",
        "status" : "interview",
        "date_applied": '2026-10-29'
    }

    create_response = client.post("/applications", json=payload2)

    assert create_response.status_code == 201

    response = client.get("/applications")

    assert response.status_code == 200
    body = response.json

    assert len(body) == 2

    # can just check this, make sure to check before popping id
    assert existing_application.json in body
    
    for app in body:
        app_id = app.pop("id", None)
        assert isinstance(app_id, int)


    assert body == [
        {
        "company": "Bosch",
        "title": "Junior Engineer",
        "status": "applied",
        "date_applied": "2026-10-26",
        "date_interview": None,
    }, 
    {
        "company": "Kaufland",
        "title": "Senior Engineer",
        "status" : "interview",
        "date_applied": '2026-10-29',
        "date_interview": None,
    }
    ]


def test_get_all_applications_empty(client):
    response = client.get("/applications")

    assert response.status_code == 200
    assert isinstance(response.json, list)
    assert response.json == []

def test_get_application_success(client, existing_application):
    app_id = existing_application.json["id"]
    response = client.get(f"/applications/{app_id}")

    assert response.status_code == 200
    assert response.json == existing_application.json

def test_get_nonexistent_application(client):
    nonexistent_app_id = NON_EXISTENT_ID
    response = client.get(f"/applications/{nonexistent_app_id}")

    assert response.status_code == 404
    assert response.json["error"] == "MISSING_ERROR"
    assert "Application not found." in response.json["details"]

def test_post_success(client):
    payload = {
        "company": "Bosch", 
        "title": "Junior Engineer", 
        "status" : "applied", 
        "date_applied": '2026-10-26'
    }

    response = client.post("/applications", json=payload)

    assert response.status_code == 201

    body = response.json
    app_id = body.pop("id", None)

    assert isinstance(app_id, int)
    assert body == {
        "company": "Bosch",
        "title": "Junior Engineer",
        "status": "applied",
        "date_applied": "2026-10-26",
        "date_interview": None,
    }

def test_post_invalid_status(client):
    payload = {
        "company": "Bosch",
        "title": "Junior Engineer",
        "status" : "INCORRECT_STATUS",
        "date_applied": '2026-10-26'
    }

    response = client.post("/applications", json=payload)

    assert response.status_code == 400
    assert response.json["error"] == "VALIDATION_ERROR"
    assert "Missing or wrong status" in response.json["details"]

def test_post_missing_field(client):
    payload = {
        # "company": "Bosch",
        "title": "Junior Engineer",
        "status" : "applied",
        "date_applied": '2026-10-26'
    }

    response = client.post("/applications", json=payload)

    assert response.status_code == 400
    assert response.json["error"] == "VALIDATION_ERROR"
    assert "Missing company" in response.json["details"]

def test_patch_success(client, existing_application):
    modified_payload = {
        "title": "Senior Software Engineer",
        "status" : "interview"
    }

    app_id = existing_application.json["id"]
    modified_application = client.patch(f"/applications/{app_id}", json=modified_payload)

    assert modified_application.status_code == 200
    assert modified_application.json["title"] == "Senior Software Engineer"
    assert modified_application.json["status"] == "interview"
    assert modified_application.json["company"] == "Bosch"
    assert modified_application.json["date_applied"] == "2026-10-26"
    assert modified_application.json["date_interview"] is None

def test_invalid_field_patch(client, existing_application):
    modified_payload = {
        "INCORRECT_FIELD": "Senior Software Engineer"
    }

    app_id = existing_application.json["id"]
    modified_application = client.patch(f"/applications/{app_id}", json=modified_payload)

    assert modified_application.status_code == 400
    assert modified_application.json["error"] == "VALIDATION_ERROR"
    assert "No valid fields provided to modify" in modified_application.json["details"]

def test_invalid_status_patch(client, existing_application):
    modified_payload = {
        "title": "Senior Software Engineer",
        "status" : "INCORRECT_STATUS"
    }

    app_id = existing_application.json["id"]
    modified_application = client.patch(f"/applications/{app_id}", json=modified_payload)

    assert modified_application.status_code == 400
    assert modified_application.json["error"] == "VALIDATION_ERROR"
    assert "Incorrect status" in modified_application.json["details"]

def test_nonexistent_patch(client):
    modified_payload = {
        "title": "Senior Software Engineer",
        "status" : "interview"
    }

    nonexistent_app_id = NON_EXISTENT_ID
    
    modified_application = client.patch(f"/applications/{nonexistent_app_id}", json=modified_payload)

    assert modified_application.status_code == 404
    assert modified_application.json["error"] == "MISSING_ERROR"
    assert "Application not found" in modified_application.json["details"]

def test_delete_success(client, existing_application):
    app_id = existing_application.json["id"]
    response = client.delete(f"/applications/{app_id}")

    assert response.status_code == 204

    response_to_fail = client.get(f"/applications/{app_id}")

    assert response_to_fail.status_code == 404
    assert response_to_fail.json["error"] == "MISSING_ERROR"
    assert "Application not found" in response_to_fail.json["details"]

def test_missing_delete(client):
    nonexistent_app_id = NON_EXISTENT_ID
    response = client.delete(f"/applications/{nonexistent_app_id}")

    assert response.status_code == 404
    assert response.json["error"] == "MISSING_ERROR"
    assert "Could not find application to delete" in response.json["details"]