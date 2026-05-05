import pytest
import uuid

from app.models.train_stop_distance import TrainStopDistanceProblem


def test_valid_straight_line_test_request(client):
    response = client.get("/api/v1/train-stop-distance/generate-problem")
    response_body = response.json()

    assert response.status_code == 200
    assert response_body["id"] is not None
    assert response_body["created_at"] is not None
    assert response_body["velocity"] is not None
    assert response_body["acceleration"] is not None


def test_train_stop_distance_request_wrote_to_database(client, wrap_the_session):
    response = client.get("/api/v1/train-stop-distance/generate-problem")
    response_body = response.json()
    db_problem = wrap_the_session.get(TrainStopDistanceProblem, response_body["id"])

    assert db_problem is not None


def test_valid_train_stop_distance_attempt(client):
    problem_response = client.get("/api/v1/train-stop-distance/generate-problem")
    problem_body = problem_response.json()

    payload = {
        "problem_id": problem_body["id"],
        "student_train_stop_distance": 8.0
    }

    attempt_response = client.post(
        "/api/v1/train-stop-distance/submit-attempt",
        json=payload
    )
    attempt_body = attempt_response.json()

    assert attempt_response.status_code == 200
    assert attempt_body["id"] is not None
    assert attempt_body["created_at"] is not None
    assert attempt_body["distance_hit"] is not None
    assert attempt_body["correct_train_stop_distance"] is not None
    assert attempt_body["train_positions"] is not None


def test_train_stop_distance_failure(client):
    payload = {
        "problem_id": str(uuid.uuid4()),
        "student_train_stop_distance": 8.0
    }

    attempt_response = client.post(
        "/api/v1/train-stop-distance/submit-attempt",
        json=payload
    )
    attempt_body = attempt_response.json()

    assert attempt_response.status_code == 404
    assert attempt_body["error"] == "Problem not found"


def test_train_stop_distance_malformed_input(client):
    payload = {
        "problem_id": "Not a UUID",
        "student_train_stop_distance": "Not a float"
    }

    attempt_response = client.post(
        "/api/v1/train-stop-distance/submit-attempt",
        json=payload
    )

    assert attempt_response.status_code == 422