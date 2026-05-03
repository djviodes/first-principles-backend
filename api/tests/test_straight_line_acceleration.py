import pytest
import uuid

from app.models.straight_line_acceleration import StraightLineAccelerationProblem


def test_valid_straight_line_test_request(client):
    response = client.get("/api/v1/straight-line-acceleration/generate-problem")
    response_body = response.json()

    assert response.status_code == 200
    assert response_body["id"] is not None
    assert response_body["created_at"] is not None
    assert response_body["distance"] is not None
    assert response_body["time"] is not None


def test_straight_line_acceleration_request_wrote_to_database(client, wrap_the_session):
    response = client.get("/api/v1/straight-line-acceleration/generate-problem")
    response_body = response.json()
    db_problem = wrap_the_session.get(StraightLineAccelerationProblem, response_body["id"])

    assert db_problem is not None


def test_valid_straight_line_acceleration_attempt(client):
    problem_response = client.get("/api/v1/straight-line-acceleration/generate-problem")
    problem_body = problem_response.json()

    payload = {
        "problem_id": problem_body["id"],
        "student_straight_line_acceleration": 8.0
    }

    attempt_response = client.post(
        "/api/v1/straight-line-acceleration/submit-attempt",
        json=payload
    )
    attempt_body = attempt_response.json()

    assert attempt_response.status_code == 200
    assert attempt_body["id"] is not None
    assert attempt_body["created_at"] is not None
    assert attempt_body["time_hit"] is not None
    assert attempt_body["correct_straight_line_acceleration"] is not None
    assert attempt_body["car_positions"] is not None


def test_straight_line_acceleration_failure(client):
    payload = {
        "problem_id": str(uuid.uuid4()),
        "student_straight_line_acceleration": 8.0
    }

    attempt_response = client.post(
        "/api/v1/straight-line-acceleration/submit-attempt",
        json=payload
    )
    attempt_body = attempt_response.json()

    assert attempt_response.status_code == 404
    assert attempt_body["error"] == "Problem not found"


def test_straight_line_acceleration_malformed_input(client):
    payload = {
        "problem_id": "Not a UUID",
        "student_straight_line_acceleration": "Not a float"
    }

    attempt_response = client.post(
        "/api/v1/straight-line-acceleration/submit-attempt",
        json=payload
    )

    assert attempt_response.status_code == 422