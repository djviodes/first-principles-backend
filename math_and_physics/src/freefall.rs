use pyo3::prelude::*;

#[pyclass]
pub struct FreeFallResult {
    #[pyo3(get)]
    pub initial_height: f64,
    #[pyo3(get)]
    pub final_height: f64,
    #[pyo3(get)]
    pub initial_velocity: f64,
    #[pyo3(get)]
    pub final_velocity: f64,
    #[pyo3(get)]
    pub acceleration: f64,
    #[pyo3(get)]
    pub time_of_flight: f64,
}

#[pyfunction]
pub fn compute_freefall(drag: bool, initial_velocity: f64) -> PyResult<FreeFallResult> {
    // TODO: implement freefall calculation
    todo!()
}