use pyo3::prelude::*;

mod drop_time;
mod straight_line_acceleration;
mod train_stop_distance;
mod bird_instantaneous_velocity;
mod relay_catchup_time;
mod squirrel_position_and_velocity_vectors;
mod river_jump_velocity;

#[pymodule]
fn math_and_physics(m: &Bound<'_, PyModule>) -> PyResult<()> {
    m.add_class::<drop_time::DropTimeResult>()?;
    m.add_class::<straight_line_acceleration::StraightLineAccelerationResult>()?;
    m.add_class::<train_stop_distance::TrainStopDistanceResult>()?;
    m.add_class::<bird_instantaneous_velocity::BirdInstantaneousVelocityResult>()?;
    m.add_class::<relay_catchup_time::RelayCatchupTimeResult>()?;
    m.add_class::<squirrel_position_and_velocity_vectors::SquirrelPartAResult>()?;
    m.add_class::<squirrel_position_and_velocity_vectors::SquirrelPartBResult>()?;
    m.add_class::<squirrel_position_and_velocity_vectors::SquirrelPartCResult>()?;
    m.add_class::<river_jump_velocity::RiverJumpVelocityPartAResult>()?;
    m.add_class::<river_jump_velocity::RiverJumpVelocityPartBResult>()?;

    m.add_function(wrap_pyfunction!(drop_time::compute_drop_time, m)?)?;
    m.add_function(wrap_pyfunction!(straight_line_acceleration::compute_straight_line_acceleration, m)?)?;
    m.add_function(wrap_pyfunction!(train_stop_distance::compute_train_stop_distance, m)?)?;
    m.add_function(wrap_pyfunction!(bird_instantaneous_velocity::compute_bird_instantaneous_velocity, m)?)?;
    m.add_function(wrap_pyfunction!(relay_catchup_time::compute_relay_catchup_time, m)?)?;
    m.add_function(wrap_pyfunction!(squirrel_position_and_velocity_vectors::compute_squirrel_part_a, m)?)?;
    m.add_function(wrap_pyfunction!(squirrel_position_and_velocity_vectors::compute_squirrel_part_b, m)?)?;
    m.add_function(wrap_pyfunction!(squirrel_position_and_velocity_vectors::compute_squirrel_part_c, m)?)?;
    m.add_function(wrap_pyfunction!(river_jump_velocity::river_jump_velocity_part_a, m)?)?;
    m.add_function(wrap_pyfunction!(river_jump_velocity::river_jump_velocity_part_b, m)?)?;

    Ok(())
}
