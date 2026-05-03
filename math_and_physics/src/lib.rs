use pyo3::prelude::*;

mod drop_time;
mod straight_line_acceleration;

#[pymodule]
fn math_and_physics(m: &Bound<'_, PyModule>) -> PyResult<()> {
    m.add_class::<drop_time::DropTimeResult>()?;
    m.add_class::<straight_line_acceleration::StraightLineAccelerationResult>()?;
    m.add_function(wrap_pyfunction!(drop_time::compute_drop_time, m)?)?;
    m.add_function(wrap_pyfunction!(straight_line_acceleration::compute_straight_line_acceleration, m)?)?;
    Ok(())
}
