import pytest
import uuid

from app.models.river_jump_velocity import RiverJumpVelocityProblem


def test_valid_river_jump_velocity_request(client):
    response = client.get("/api/v1/river-jump-velocity/generate-problem")
    response_body = response.json()

    assert response.status_code == 200
    assert response_body["id"] is not None
    assert response_body["created_at"] is not None
    assert isinstance(response_body["x_f"], float)
    assert isinstance(response_body["y_i"], float)
    assert isinstance(response_body["y_f"], float)


def test_river_jump_velocity_request_wrote_to_database(
    client,
    wrap_the_session
):
    response = client.get("/api/v1/river-jump-velocity/generate-problem")
    response_body = response.json()
    db_problem = wrap_the_session.get(RiverJumpVelocityProblem, response_body["id"])

    assert db_problem is not None


def test_valid_river_jump_velocity_attempt_a(client):
    problem_response = client.get("/api/v1/river-jump-velocity/generate-problem")
    problem_body = problem_response.json()

    payload = {
        "problem_id": problem_body["id"],
        "student_x_velocity": 25.0
    }

    attempt_response = client.post(
        "/api/v1/river-jump-velocity/submit-attempt-a",
        json=payload
    )
    attempt_body = attempt_response.json()

    assert attempt_response.status_code == 200
    assert attempt_body["id"] is not None
    assert attempt_body["created_at"] is not None
    assert isinstance(attempt_body["velocity_hit"], bool)


def test_failed_river_jump_velocity_attempt_a(client):
    payload = {
        "problem_id": str(uuid.uuid4()),
        "student_x_velocity": 25.0
    }

    attempt_response = client.post(
        "/api/v1/river-jump-velocity/submit-attempt-a",
        json=payload
    )

    assert attempt_response.status_code == 404


def test_valid_river_jump_velocity_attempt_b(client):
    problem_response = client.get("/api/v1/river-jump-velocity/generate-problem")
    problem_body = problem_response.json()

    payload = {
        "problem_id": problem_body["id"],
        "student_final_velocity": 33.0
    }

    attempt_response = client.post(
        "/api/v1/river-jump-velocity/submit-attempt-b",
        json=payload
    )
    attempt_body = attempt_response.json()

    assert attempt_response.status_code == 200
    assert attempt_body["id"] is not None
    assert attempt_body["created_at"] is not None
    assert isinstance(attempt_body["final_velocity_hit"], bool)


def test_failed_river_jump_velocity_attempt_b(client):
    payload = {
        "problem_id": str(uuid.uuid4()),
        "student_final_velocity": 33.0
    }

    attempt_response = client.post(
        "/api/v1/river-jump-velocity/submit-attempt-b",
        json=payload
    )
    attempt_body = attempt_response.json()

    assert attempt_response.status_code == 404
    assert attempt_body["error"] == "Problem not found"