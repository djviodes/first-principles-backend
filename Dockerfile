# Stage 1: Build Rust library
FROM rust:1.95 AS rust-builder
WORKDIR /math_and_physics

RUN apt-get update && apt-get install -y python3 python3-pip python3-dev
RUN pip3 install maturin --break-system-packages

COPY math_and_physics/Cargo.toml ./Cargo.toml
COPY math_and_physics/src ./src

RUN PYO3_USE_ABI3_FORWARD_COMPATIBILITY=1 maturin build --release --features pyo3/abi3-py311

# Stage 2: Python API
FROM python:3.11
WORKDIR /app

COPY --from=rust-builder /math_and_physics/target/wheels/*.whl ./
RUN pip install *.whl

COPY api/pyproject.toml ./pyproject.toml
COPY api/app ./app

RUN pip install .

EXPOSE 8000

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]