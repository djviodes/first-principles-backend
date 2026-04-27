use pyo3::prelude::*;

#[pyclass]
pub struct DropTimeResult {
    #[pyo3(get)]
    pub hit: bool,
    #[pyo3(get)]
    pub correct_drop_time: f64,
    #[pyo3(get)]
    pub balloon_positions: Vec<f64>,
    #[pyo3(get)]
    pub walker_positions: Vec<f64>,
}

fn compute_drop_time_logic(
    input_drop_time: f64,
    height: f64,
    walker_start: f64,
    walker_velocity: f64,
) -> DropTimeResult {
    let dt: f64 = 1.0 / 60.0;
    let t_total: f64 = walker_start / -walker_velocity;
    let mut balloon_positions: Vec<f64> = vec![];
    let mut walker_positions: Vec<f64> = vec![];

    let mut t: f64 = 0.0;
    while t <= t_total {
        let walker_position: f64 = walker_start + (walker_velocity * t);
        let balloon_position: f64;
        if t < input_drop_time {
            balloon_position = height;
        } else {
            let t_since_drop: f64 = t - input_drop_time;
            balloon_position = height - (0.5 * 9.81 * t_since_drop.powi(2));
        }

        walker_positions.push(walker_position);
        balloon_positions.push(balloon_position);

        t += dt;
    }

    let correct_drop_time: f64 = (t_total) - ((2.0 * height) / 9.81).sqrt();
    let rounded_correct_drop_time = (correct_drop_time * 10.0).round() / 10.0;
    let student_drop_time = (input_drop_time * 10.0).round() / 10.0;

    if student_drop_time == rounded_correct_drop_time {
        DropTimeResult{
            hit: true,
            correct_drop_time: rounded_correct_drop_time,
            balloon_positions: balloon_positions,
            walker_positions: walker_positions,
        }
    } else {
        DropTimeResult{
            hit: false,
            correct_drop_time: rounded_correct_drop_time,
            balloon_positions: balloon_positions,
            walker_positions: walker_positions,
        }
    }
}

#[pyfunction]
pub fn compute_drop_time(
    input_drop_time: f64,
    height: f64,
    walker_start: f64,
    walker_velocity: f64,
) -> PyResult<DropTimeResult> {
    Ok(compute_drop_time_logic(
        input_drop_time,
        height,
        walker_start,
        walker_velocity,
    ))
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_valid_compute_drop_time_logic() {
        const HEIGHT: f64 = 20.0;
        const WALKER_START: f64 = 10.0;
        const WALKER_VELOCITY: f64 = -2.0;
    
        let drop_time_calculation: DropTimeResult = compute_drop_time_logic(
            3.0,
            HEIGHT,
            WALKER_START, 
            WALKER_VELOCITY
        );

        assert!(drop_time_calculation.hit);
        assert_eq!(drop_time_calculation.correct_drop_time, 3.0);
        assert!(drop_time_calculation.balloon_positions.len() > 0);
        assert!(drop_time_calculation.walker_positions.len() > 0);
    }

    #[test]
    fn test_failed_compute_drop_time_logic() {
        const HEIGHT: f64 = 20.0;
        const WALKER_START: f64 = 10.0;
        const WALKER_VELOCITY: f64 = -2.0;

        let drop_time_calculation: DropTimeResult = compute_drop_time_logic(
            5.0,
            HEIGHT, 
            WALKER_START,
            WALKER_VELOCITY
        );

        assert!(!drop_time_calculation.hit);
        assert_eq!(drop_time_calculation.correct_drop_time, 3.0);
    }
}