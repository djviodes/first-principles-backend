import pytest
import uuid

from app.models.squirrel_position_and_velocity_vectors import SquirrelPositionAndVelocityProblem


def test_valid_squirrel_position_and_velocity_request(client):
    response = client.get("/api/v1/squirrel-position-and-velocity/generate-problem")
    response_body = response.json()

    assert response.status_code == 200
    assert response_body["id"] is not None
    assert response_body["created_at"] is not None
    assert isinstance(response_body["a_x"], float)
    assert isinstance(response_body["b_x"], float)
    assert isinstance(response_body["c_y"], float)
    assert isinstance(response_body["time"], float)


def test_squirrel_position_and_velocity_request_wrote_to_database(
    client,
    wrap_the_session
):
    response = client.get("/api/v1/squirrel-position-and-velocity/generate-problem")
    response_body = response.json()
    db_problem = wrap_the_session.get(SquirrelPositionAndVelocityProblem, response_body["id"])

    assert db_problem is not None


def test_valid_squirrel_position_and_velocity_attempt_a(client):
    problem_response = client.get("/api/v1/squirrel-position-and-velocity/generate-problem")
    problem_body = problem_response.json()

    payload = {
        "problem_id": problem_body["id"],
        "student_a_x": 0.280,
        "student_b_x": 0.0360,
        "student_c_y": 0.0190
    }

    attempt_response = client.post(
        "/api/v1/squirrel-position-and-velocity/submit-attempt-a",
        json=payload
    )
    attempt_body = attempt_response.json()

    assert attempt_response.status_code == 200
    assert attempt_body["id"] is not None
    assert attempt_body["created_at"] is not None
    assert isinstance(attempt_body["coefficient_hit"], bool)
    assert isinstance(attempt_body["squirrel_x_positions"], list)
    assert len(attempt_body["squirrel_x_positions"]) > 0
    assert isinstance(attempt_body["squirrel_y_positions"], list)
    assert len(attempt_body["squirrel_y_positions"]) > 0


def test_failed_squirrel_position_and_velocity_attempt_a(client):
    payload = {
        "problem_id": str(uuid.uuid4()),
        "student_a_x": 0.280,
        "student_b_x": 0.0360,
        "student_c_y": 0.0190
    }

    attempt_response = client.post(
        "/api/v1/squirrel-position-and-velocity/submit-attempt-a",
        json=payload
    )
    attempt_body = attempt_response.json()

    assert attempt_response.status_code == 404
    assert attempt_body["error"] == "Problem not found"


def test_squirrel_position_and_velocity_attempt_a_malformed_input(client):
    payload = {
        "problem_id": "Not a UUID",
        "student_a_x": "Not a float",
        "student_b_x": "Not a float",
        "student_c_y": "Not a float"
    }

    attempt_response = client.post(
        "/api/v1/squirrel-position-and-velocity/submit-attempt-a",
        json=payload
    )

    assert attempt_response.status_code == 422


def test_valid_squirrel_position_and_velocity_attempt_b(client):
    problem_response = client.get("/api/v1/squirrel-position-and-velocity/generate-problem")
    problem_body = problem_response.json()

    payload = {
        "problem_id": problem_body["id"],
        "student_distance": 5.0
    }

    attempt_response = client.post(
        "/api/v1/squirrel-position-and-velocity/submit-attempt-b",
        json=payload
    )
    attempt_body = attempt_response.json()

    assert attempt_response.status_code == 200
    assert attempt_body["id"] is not None
    assert attempt_body["created_at"] is not None
    assert isinstance(attempt_body["distance_hit"], bool)


def test_failed_squirrel_position_and_velocity_attempt_b(client):
    payload = {
        "problem_id": str(uuid.uuid4()),
        "student_distance": 5.0
    }

    attempt_response = client.post(
        "/api/v1/squirrel-position-and-velocity/submit-attempt-b",
        json=payload
    )
    attempt_body = attempt_response.json()

    assert attempt_response.status_code == 404
    assert attempt_body["error"] == "Problem not found"


def test_squirrel_position_and_velocity_attempt_b_malformed_input(client):
    payload = {
        "problem_id": "Not a UUID",
        "student_distance": "Not a float"
    }

    attempt_response = client.post(
        "/api/v1/squirrel-position-and-velocity/submit-attempt-b",
        json=payload
    )

    assert attempt_response.status_code == 422


def test_valid_squirrel_position_and_velocity_attempt_c(client):
    problem_response = client.get("/api/v1/squirrel-position-and-velocity/generate-problem")
    problem_body = problem_response.json()

    payload = {
        "problem_id": problem_body["id"],
        "student_magnitude": 5.0,
        "student_direction": 60.0
    }

    attempt_response = client.post(
        "/api/v1/squirrel-position-and-velocity/submit-attempt-c",
        json=payload
    )
    attempt_body = attempt_response.json()

    assert attempt_response.status_code == 200
    assert attempt_body["id"] is not None
    assert attempt_body["created_at"] is not None
    assert isinstance(attempt_body["magnitude_and_direction_hit"], bool)


def test_failed_squirrel_position_and_velocity_attempt_c(client):
    payload = {
        "problem_id": str(uuid.uuid4()),
        "student_magnitude": 5.0,
        "student_direction": 60.0
    }

    attempt_response = client.post(
        "/api/v1/squirrel-position-and-velocity/submit-attempt-c",
        json=payload
    )
    attempt_body = attempt_response.json()

    assert attempt_response.status_code == 404
    assert attempt_body["error"] == "Problem not found"


def test_squirrel_position_and_velocity_attempt_c_malformed_input(client):
    payload = {
        "problem_id": "Not a UUID",
        "student_magnitude": "Not a float",
        "student_direction": "Not a float"
    }

    attempt_response = client.post(
        "/api/v1/squirrel-position-and-velocity/submit-attempt-c",
        json=payload
    )

    assert attempt_response.status_code == 422