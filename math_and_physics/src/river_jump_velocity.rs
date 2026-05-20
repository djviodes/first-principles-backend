use pyo3::prelude::*;

#[pyclass]
pub struct RiverJumpVelocityPartAResult {
    #[pyo3(get)]
    pub hit: bool,
    #[pyo3(get)]
    pub correct_x_velocity: f64,
    #[pyo3(get)]
    pub car_x_positions: Vec<f64>,
    #[pyo3(get)]
    pub car_y_positions: Vec<f64>,
}

#[pyclass]
pub struct RiverJumpVelocityPartBResult {
    #[pyo3(get)]
    pub hit: bool,
    #[pyo3(get)]
    pub correct_final_velocity: f64,
}

fn compute_river_jump_velocity_part_a_logic(
    input_x_velocity: f64,
    x_f: f64,
    y_i: f64,
    y_f: f64,
) -> RiverJumpVelocityPartAResult {
    let dt: f64 = 1.0 / 60.0;
    let mut car_x_positions: Vec<f64> = vec![];
    let mut car_y_positions: Vec<f64> = vec![];

    let jump_time: f64 = ((y_f - y_i) / (0.5 * -9.81)).sqrt();
    let correct_x_velocity: f64 = x_f / jump_time;
    let rounded_correct_x_velocity: f64 = correct_x_velocity.round();
    let student_x_velocity: f64 = input_x_velocity.round();

    let mut t: f64 = 0.0;
    loop {
        let x_position: f64 = student_x_velocity * t;
        let y_position: f64 = y_i + 0.5 * -9.81 * t.powi(2);

        car_x_positions.push(x_position);
        car_y_positions.push(y_position);

        if x_position >= x_f || y_position <= y_f {
            break;
        }

        t += dt;
    }

    RiverJumpVelocityPartAResult{
        hit: student_x_velocity == rounded_correct_x_velocity,
        correct_x_velocity: rounded_correct_x_velocity,
        car_x_positions,
        car_y_positions
    }
}

fn compute_river_jump_velocity_part_b_logic(
    input_final_velocity: f64,
    x_f: f64,
    y_i: f64,
    y_f: f64,
) -> RiverJumpVelocityPartBResult {
    let jump_time: f64 = ((y_f - y_i) / (0.5 * -9.81)).sqrt();
    let x_velocity: f64 = x_f / jump_time;
    let y_velocity: f64 = -9.81 * jump_time;
    let correct_final_velocity: f64 = (x_velocity.powi(2) + y_velocity.powi(2)).sqrt();
    let rounded_correct_final_velocity: f64 = correct_final_velocity.round();
    let student_final_velocity: f64 = input_final_velocity.round();

    RiverJumpVelocityPartBResult{
        hit: student_final_velocity == rounded_correct_final_velocity,
        correct_final_velocity: rounded_correct_final_velocity
    }
}

#[pyfunction]
pub fn river_jump_velocity_part_a(
    input_x_velocity: f64,
    x_f: f64,
    y_i: f64,
    y_f: f64,
) -> PyResult<RiverJumpVelocityPartAResult> {
    Ok(compute_river_jump_velocity_part_a_logic(input_x_velocity, x_f, y_i, y_f))
}

#[pyfunction]
pub fn river_jump_velocity_part_b(
    input_final_velocity: f64,
    x_f: f64,
    y_i: f64,
    y_f: f64,
) -> PyResult<RiverJumpVelocityPartBResult> {
    Ok(compute_river_jump_velocity_part_b_logic(input_final_velocity, x_f, y_i, y_f))
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_valid_river_jump_velocity_part_a() {
        const X_F: f64 = 53.0;
        const Y_I: f64 = 26.3;
        const Y_F: f64 = 4.5;

        let river_jump_velocity_part_a_calculation: RiverJumpVelocityPartAResult = compute_river_jump_velocity_part_a_logic(
            25.0,
            X_F,
            Y_I,
            Y_F
        );

        assert!(river_jump_velocity_part_a_calculation.hit);
        assert_eq!(river_jump_velocity_part_a_calculation.correct_x_velocity, 25.0);
        assert!(river_jump_velocity_part_a_calculation.car_x_positions.len() > 0);
        assert!(river_jump_velocity_part_a_calculation.car_y_positions.len() > 0);
    }

    #[test]
    fn test_failed_river_jump_velocity_part_a() {
        const X_F: f64 = 53.0;
        const Y_I: f64 = 26.3;
        const Y_F: f64 = 4.5;

        let river_jump_velocity_part_a_calculation: RiverJumpVelocityPartAResult = compute_river_jump_velocity_part_a_logic(
            24.0,
            X_F,
            Y_I,
            Y_F
        );

        assert!(!river_jump_velocity_part_a_calculation.hit);
        assert_eq!(river_jump_velocity_part_a_calculation.correct_x_velocity, 25.0);
    }

    #[test]
    fn test_valid_river_jump_velocity_part_b() {
        const X_F: f64 = 53.0;
        const Y_I: f64 = 26.3;
        const Y_F: f64 = 4.5;

        let river_jump_velocity_part_b_calculation: RiverJumpVelocityPartBResult = compute_river_jump_velocity_part_b_logic(
            33.0,
            X_F,
            Y_I,
            Y_F
        );

        assert!(river_jump_velocity_part_b_calculation.hit);
        assert_eq!(river_jump_velocity_part_b_calculation.correct_final_velocity, 33.0);
    }

    #[test]
    fn test_failed_river_jump_velocity_part_b() {
        const X_F: f64 = 53.0;
        const Y_I: f64 = 26.3;
        const Y_F: f64 = 4.5;

        let river_jump_velocity_part_b_calculation: RiverJumpVelocityPartBResult = compute_river_jump_velocity_part_b_logic(
            32.0,
            X_F,
            Y_I,
            Y_F
        );

        assert!(!river_jump_velocity_part_b_calculation.hit);
        assert_eq!(river_jump_velocity_part_b_calculation.correct_final_velocity, 33.0);
    }
}