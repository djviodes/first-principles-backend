import pytest
import uuid

from app.models.bird_instantaneous_velocity import BirdInstantaneousVelocityProblem


def test_valid_bird_instantaneous_velocity_request(client):
    response = client.get("/api/v1/bird-instantaneous-velocity/generate-problem")
    response_body = response.json()

    assert response.status_code == 200
    assert response_body["id"] is not None
    assert response_body["created_at"] is not None
    assert response_body["function_type"] is not None
    assert response_body["time"] is not None
    assert response_body["a"] is not None
    assert response_body["b"] is not None

    match response_body["function_type"]:
        case "quadratic":
            assert response_body["c"] is not None
        case "cubic":
            assert response_body["c"] is not None
            assert response_body["d"] is not None


def test_bird_instantaneous_velocity_request_wrote_to_database(client, wrap_the_session):
    response = client.get("/api/v1/bird-instantaneous-velocity/generate-problem")
    response_body = response.json()
    db_problem = wrap_the_session.get(BirdInstantaneousVelocityProblem, response_body["id"])

    assert db_problem is not None


def test_valid_bird_instantaneous_velocity_attempt(client):
    problem_response = client.get("/api/v1/bird-instantaneous-velocity/generate-problem")
    problem_body = problem_response.json()

    payload = {
        "problem_id": problem_body["id"],
        "student_bird_instantaneous_velocity": 8.0
    }

    attempt_response = client.post(
        "/api/v1/bird-instantaneous-velocity/submit-attempt",
        json=payload
    )
    attempt_body = attempt_response.json()

    assert attempt_response.status_code == 200
    assert attempt_body["id"] is not None
    assert attempt_body["created_at"] is not None
    assert attempt_body["velocity_hit"] is not None
    assert attempt_body["correct_bird_instantaneous_velocity"] is not None
    assert attempt_body["bird_positions"] is not None


def test_bird_instantaneous_velocity_failure(client):
    payload = {
        "problem_id": str(uuid.uuid4()),
        "student_bird_instantaneous_velocity": 8.0
    }

    attempt_response = client.post(
        "/api/v1/bird-instantaneous-velocity/submit-attempt",
        json=payload
    )
    attempt_body = attempt_response.json()

    assert attempt_response.status_code == 404
    assert attempt_body["error"] == "Problem not found"


def test_bird_instantaneous_velocity_malformed_input(client):
    payload = {
        "problem_id": "Not a UUID",
        "student_bird_instantaneous_velocity": "Not a float"
    }

    attempt_response = client.post(
        "/api/v1/bird-instantaneous-velocity/submit-attempt",
        json=payload
    )

    assert attempt_response.status_code == 422