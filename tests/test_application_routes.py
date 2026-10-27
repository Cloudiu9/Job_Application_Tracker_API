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
    return response.json

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
    assert existing_application in body
    
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
    app_id = existing_application["id"]
    response = client.get(f"/applications/{app_id}")

    assert response.status_code == 200
    assert response.json == existing_application

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

@pytest.mark.parametrize("payload, expected_status, expected_error, expected_details", [
    ({
        "company": "Bosch",
        "title": "Junior Engineer",
        "status" : "INCORRECT_STATUS",
        "date_applied": '2026-10-26'
    }, 
    400,
    "VALIDATION_ERROR",
    "Missing or wrong status"
    ),
    ({
        # "company": "Bosch",
        "title": "Junior Engineer",
        "status" : "applied",
        "date_applied": '2026-10-26'
    }, 
    400,
    "VALIDATION_ERROR",
    "Missing company"
    ),
])
def test_post_failure(client, payload, expected_status, expected_error, expected_details):
    response = client.post("/applications", json=payload)

    assert response.status_code == expected_status
    assert response.json["error"] == expected_error
    assert expected_details in response.json["details"]


def test_patch_success(client, existing_application):
    modified_payload = {
        "title": "Senior Software Engineer",
        "status" : "interview"
    }

    app_id = existing_application["id"]
    modified_application = client.patch(f"/applications/{app_id}", json=modified_payload)

    assert modified_application.status_code == 200
    assert modified_application.json["title"] == "Senior Software Engineer"
    assert modified_application.json["status"] == "interview"
    assert modified_application.json["company"] == "Bosch"
    assert modified_application.json["date_applied"] == "2026-10-26"
    assert modified_application.json["date_interview"] is None

@pytest.mark.parametrize("payload, expected_status, expected_error, expected_details", [
    ({
        "INCORRECT_FIELD": "Senior Software Engineer"
    }, 
    400,
    "VALIDATION_ERROR",
    "No valid fields provided to modify"
    ),
    ({
        "title": "Senior Software Engineer",
        "status" : "INCORRECT_STATUS"
    }, 
    400,
    "VALIDATION_ERROR",
    "Incorrect status"
    ),
])
def test_patch_failure(client, existing_application, payload, expected_status, expected_error, expected_details):
    app_id = existing_application["id"]
    modified_application = client.patch(f"/applications/{app_id}", json=payload)

    assert modified_application.status_code == expected_status
    assert modified_application.json["error"] == expected_error
    assert expected_details in modified_application.json["details"]

def test_nonexistent_patch(client):
    modified_payload = {
        "title": "Senior Software Engineer",
        "status" : "interview"
    }
    
    modified_application = client.patch(f"/applications/{NON_EXISTENT_ID}", json=modified_payload)

    assert modified_application.status_code == 404
    assert modified_application.json["error"] == "MISSING_ERROR"
    assert "Application not found" in modified_application.json["details"]

def test_delete_success(client, existing_application):
    app_id = existing_application["id"]
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