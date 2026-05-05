use pyo3::prelude::*;

#[pyclass]
pub struct TrainStopDistanceResult {
    #[pyo3(get)]
    pub hit: bool,
    #[pyo3(get)]
    pub correct_stopping_distance: f64,
    #[pyo3(get)]
    pub train_positions: Vec<f64>,
}

fn compute_train_stop_distance_logic(
    input_distance: f64,
    train_velocity: f64,
    train_deceleration: f64,
) -> TrainStopDistanceResult {
    let dt: f64 = 1.0 / 60.0;
    let mut train_positions: Vec<f64> = vec![];

    let correct_train_stop_distance: f64 = train_velocity.powi(2) / (2.0 * train_deceleration);
    let rounded_correct_train_stop_distance: f64 = (correct_train_stop_distance * 10.0).round() / 10.0;
    let student_train_stop_distance: f64 = (-input_distance * 10.0).round() / 10.0;

    let time: f64 = -train_velocity / train_deceleration;

    let mut t: f64 = 0.0;
    while t <= time {
        let train_position: f64 =
            input_distance
            + (train_velocity * t)
            + (0.5 * train_deceleration * t.powi(2));

        train_positions.push(train_position);

        t += dt;
    }

    if student_train_stop_distance == rounded_correct_train_stop_distance {
        TrainStopDistanceResult{
            hit: true,
            correct_stopping_distance: rounded_correct_train_stop_distance,
            train_positions: train_positions
        }
    } else {
        TrainStopDistanceResult{
            hit: false,
            correct_stopping_distance: rounded_correct_train_stop_distance,
            train_positions: train_positions
        }
    }
}

#[pyfunction]
pub fn compute_train_stop_distance(
    input_distance: f64,
    train_velocity: f64,
    train_deceleration: f64,
) -> PyResult<TrainStopDistanceResult> {
    Ok(compute_train_stop_distance_logic(
        input_distance,
        train_velocity,
        train_deceleration,
    ))
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_valid_compute_train_stop_distance_logic() {
        const TRAIN_VELOCITY: f64 = 19.45;
        const TRAIN_DECELERATION: f64 = -0.18;

        let distance_calculation: TrainStopDistanceResult = compute_train_stop_distance_logic(
            1050.8,
            TRAIN_VELOCITY,
            TRAIN_DECELERATION
        );

        assert!(distance_calculation.hit);
        assert_eq!(distance_calculation.correct_stopping_distance, -1050.8);
        assert!(distance_calculation.train_positions.len() > 0);
    }

    #[test]
    fn test_failed_compute_train_stop_distance_logic() {
        const TRAIN_VELOCITY: f64 = 19.45;
        const TRAIN_DECELERATION: f64 = -0.18;

        let distance_calculation: TrainStopDistanceResult = compute_train_stop_distance_logic(
            950.8,
            TRAIN_VELOCITY,
            TRAIN_DECELERATION
        );

        assert!(!distance_calculation.hit);
        assert_eq!(distance_calculation.correct_stopping_distance, -1050.8);
    }
}