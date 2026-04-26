use pyo3::prelude::*;

mod drop_time;

#[pymodule]
fn math_and_physics(m: &Bound<'_, PyModule>) -> PyResult<()> {
    m.add_class::<drop_time::DropTimeResult>()?;
    m.add_function(wrap_pyfunction!(drop_time::compute_drop_time, m)?)?;
    Ok(())
}
