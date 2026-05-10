import pytest
import uuid

from app.models.relay_catchup_time import RelayCatchupTimeProblem


def test_valid_relay_catchup_time_request(client):
    response = client.get("/api/v1/relay-catchup-time/generate-problem")
    response_body = response.json()

    assert response.status_code == 200
    assert response_body["id"] is not None
    assert response_body["created_at"] is not None
    assert response_body["a"] is not None
    assert response_body["b_one"] is not None
    assert response_body["b_two"] is not None
    assert response_body["v_one"] is not None
    assert response_body["v_two"] is not None
    assert response_body["s_one"] is not None
    assert response_body["s_two"] is not None


def test_relay_catchup_time_request_wrote_to_database(client, wrap_the_session):
    response = client.get("/api/v1/relay-catchup-time/generate-problem")
    response_body = response.json()
    db_problem = wrap_the_session.get(RelayCatchupTimeProblem, response_body["id"])

    assert db_problem is not None


def test_valid_relay_catchup_time_attempt(client):
    problem_response = client.get("/api/v1/relay-catchup-time/generate-problem")
    problem_body = problem_response.json()

    payload = {
        "problem_id": problem_body["id"],
        "student_relay_catchup_time": 3.5
    }

    attempt_response = client.post("/api/v1/relay-catchup-time/submit-attempt", json=payload)
    attempt_body = attempt_response.json()

    assert attempt_response.status_code == 200
    assert attempt_body["id"] is not None
    assert attempt_body["created_at"] is not None
    assert attempt_body["time_hit"] is not None
    assert attempt_body["correct_relay_catchup_time"] is not None
    assert attempt_body["runner_one_positions"] is not None
    assert attempt_body["runner_two_positions"] is not None


def test_relay_catchup_time_attempt_failure(client):
    payload = {
        "problem_id": str(uuid.uuid4()),
        "student_relay_catchup_time": 3.5
    }

    attempt_response = client.post("/api/v1/relay-catchup-time/submit-attempt", json=payload)
    attempt_body = attempt_response.json()

    assert attempt_response.status_code == 404
    assert attempt_body["error"] == "Problem not found"


def test_relay_catchup_time_attempt_malformed_input(client):
    payload = {
        "problem_id": "Not a UUID",
        "student_relay_catchup_time": "Not a float"
    }

    attempt_response = client.post("/api/v1/relay-catchup-time/submit-attempt", json=payload)

    assert attempt_response.status_code == 422