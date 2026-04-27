import pytest
import uuid

from app.models.drop_time import DropTimeProblem


def test_valid_drop_time_request(client):
    response = client.get("/api/v1/drop-time/generate-problem")
    response_body = response.json()

    assert response.status_code == 200
    assert response_body["id"] is not None
    assert response_body["created_at"] is not None
    assert response_body["height"] is not None
    assert response_body["walker_start"] is not None
    assert response_body["walker_velocity"] is not None


def test_drop_time_request_wrote_to_database(client, wrap_the_session):
    response = client.get("/api/v1/drop-time/generate-problem")
    response_body = response.json()
    db_problem = wrap_the_session.get(DropTimeProblem, response_body["id"])

    assert db_problem is not None


def test_valid_drop_time_attempt(client):
    problem_response = client.get("/api/v1/drop-time/generate-problem")
    problem_body = problem_response.json()

    payload = {
        "problem_id": problem_body["id"],
        "student_drop_time": 1.5
    }

    attempt_response = client.post("/api/v1/drop-time/submit-attempt", json=payload)
    attempt_body = attempt_response.json()

    assert attempt_response.status_code == 200
    assert attempt_body["id"] is not None
    assert attempt_body["created_at"] is not None
    assert attempt_body["target_hit"] is not None
    assert attempt_body["correct_drop_time"] is not None
    assert attempt_body["balloon_positions"] is not None
    assert attempt_body["walker_positions"] is not None


def test_drop_time_attempt_failure(client):
    payload = {
        "problem_id": str(uuid.uuid4()),
        "student_drop_time": 1.5
    }

    attempt_response = client.post("/api/v1/drop-time/submit-attempt", json=payload)
    attempt_body = attempt_response.json()

    assert attempt_response.status_code == 404
    assert attempt_body["error"] == "Problem not found"


def test_drop_time_attempt_malformed_input(client):
    payload = {
        "problem_id": "Not a UUID",
        "student_drop_time": "Not a float"
    }

    attempt_response = client.post("/api/v1/drop-time/submit-attempt", json=payload)

    assert attempt_response.status_code == 422