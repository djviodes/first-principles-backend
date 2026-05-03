# First-Principles

[![Run Tests](https://github.com/djviodes/first-principles-backend/actions/workflows/test.yml/badge.svg)](https://github.com/djviodes/first-principles-backend/actions/workflows/test.yml)

A physics study tool that aims to assist students and physics enthusiasts alike gain a better intuitive grasp on the inner workings of the equations they are learning.

---

## Features

- Allows users to calculate the amount of time it takes for a water balloon to drop on a person walking below
- Keeps all simulations realistic by displaying accurate representations of a water balloon dropping and a person walking below
- Randomizes the variables of each problem so the user is not solving the same problem twice

---

## Prerequisites

- Python >=3.11
- Rust >=1.95.0
- Docker >=29.4.0

---

## Environment Variables

```
DATABASE_URL=postgresql://<user>:<password>@<host>:<port>/<database>
LOG_LEVEL=INFO
```

---

## Installation

1. Clone the repository
```bash
git clone https://github.com/djviodes/first-principles-backend.git
cd first-principles-backend
```

2. Start the services with Docker Compose
```bash
docker compose up -d
```

3. Start up the Python virtual environment
```bash
cd api
source .venv/bin/activate
```

4. Install Python dependencies
```bash
pip install -e ".[dev]"
```

5. Build the Rust extension
```bash
cd ../math_and_physics
maturin develop
```

6. Run the migration
```bash
cd ../api
alembic upgrade head
```

---

## Running Tests

- To run the API tests, start in the root directory and run the following commands:
```bash
cd api
pytest
```

- To run the Rust equation tests, start in the root directory and run the following commands:
```bash
cd math_and_physics
cargo test
```

---

## Usage

Basic usage:
```bash
curl http://localhost:8000/api/v1/drop-time/generate-problem
```

- Here you will need to grab the `problem_id` you received from the curl request to be used in the next curl request

```bash
curl -X POST \
  -H "Content-Type: application/json" \
  -d '{"problem_id": "<<problem_id>>", "student_drop_time": "<<Float>>"}' \
  http://localhost:8000/api/v1/drop-time/submit-attempt
```

- `student_drop_time` is the float value that the user will be passing in to see if they did their calculation correctly. For testing purposes, put anything around 5.0

---

## How It Works

First-Principles generates physics based problems for users to solve and check their answers against. The user receives randomized values for the specific problem they have chosen. They are then tasked with solving for the missing variable. Once they have their answer, they submit it to be checked by a physics engine written in Rust and exposed to Python via PyO3. If they are right, they will be shown an animation indicating their success. If they are wrong, they will be shown an animation relaying that.

---

## Troubleshooting

There is a possibility that when you go to run `docker compose up -d`, you run into errors with the python versioning for the project. If you come across this, please ensure that the Dockerfile explicitly uses Python 3.11. Make sure that the `maturin build` line is:

```
RUN PYO3_USE_ABI3_FORWARD_COMPATIBILITY=1 maturin build --release --features pyo3/abi3-py311
```