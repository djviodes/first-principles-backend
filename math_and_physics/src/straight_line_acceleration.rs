use pyo3::prelude::*;

#[pyclass]
pub struct StraightLineAccelerationResult {
    #[pyo3(get)]
    pub hit: bool,
    #[pyo3(get)]
    pub correct_straight_line_acceleration: f64,
    #[pyo3(get)]
    pub car_positions: Vec<f64>,
}

fn compute_straight_line_acceleration_logic(
    input_acceleration: f64,
    distance: f64,
    time: f64,
) -> StraightLineAccelerationResult {
    let dt: f64 = 1.0 / 60.0;
    let mut car_positions: Vec<f64> = vec![];

    let correct_straight_line_acceleration: f64 = (2.0 * distance) / (time.powi(2));
    let rounded_correct_straight_line_acceleration: f64 = (correct_straight_line_acceleration * 10.0).round() / 10.0;
    let student_straight_line_acceleration: f64 = (input_acceleration * 10.0).round() / 10.0;

    let mut t: f64 = 0.0;
    while t <= time {
        let car_position: f64 = 0.5 * input_acceleration * t.powi(2);

        car_positions.push(car_position);

        t += dt;
    }

    if student_straight_line_acceleration == rounded_correct_straight_line_acceleration {
        StraightLineAccelerationResult{
            hit: true,
            correct_straight_line_acceleration: rounded_correct_straight_line_acceleration,
            car_positions: car_positions,
        }
    } else {
        StraightLineAccelerationResult{
            hit: false,
            correct_straight_line_acceleration: rounded_correct_straight_line_acceleration,
            car_positions: car_positions,
        }
    }
}

#[pyfunction]
pub fn compute_straight_line_acceleration(
    input_acceleration: f64,
    distance: f64,
    time: f64,
) -> PyResult<StraightLineAccelerationResult> {
    Ok(compute_straight_line_acceleration_logic(
        input_acceleration,
        distance,
        time,
    ))
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_valid_compute_straight_line_acceleration_logic() {
        const DISTANCE: f64 = 100.0;
        const TIME: f64 = 5.0;

        let acceleration_calculation: StraightLineAccelerationResult = compute_straight_line_acceleration_logic(
            8.0,
            DISTANCE,
            TIME
        );

        assert!(acceleration_calculation.hit);
        assert_eq!(acceleration_calculation.correct_straight_line_acceleration, 8.0);
        assert!(acceleration_calculation.car_positions.len() > 0);
    }

    #[test]
    fn test_failed_compute_straight_line_acceleration_logic() {
        const DISTANCE: f64 = 100.0;
        const TIME: f64 = 5.0;

        let acceleration_calculation: StraightLineAccelerationResult = compute_straight_line_acceleration_logic(
            7.0,
            DISTANCE,
            TIME
        );

        assert!(!acceleration_calculation.hit);
        assert_eq!(acceleration_calculation.correct_straight_line_acceleration, 8.0);
    }
}