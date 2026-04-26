use pyo3::prelude::*;

mod freefall;

#[pymodule]
fn math_and_physics(m: &Bound<'_, PyModule>) -> PyResult<()> {
    m.add_class::<freefall::FreeFallResult>()?;
    m.add_function(wrap_pyfunction!(freefall::compute_freefall, m)?)?;
    Ok(())
}
