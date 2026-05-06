use pyo3::prelude::*;

#[pyclass]
pub struct BirdInstantaneousVelocityResult {
    #[pyo3(get)]
    pub hit: bool,
    #[pyo3(get)]
    pub correct_instantaneous_velocity: f64,
    #[pyo3(get)]
    pub bird_positions: Vec<f64>,
}

fn compute_bird_instantaneous_velocity_logic(
    input_instantaneous_velocity: f64,
    function_type: &str,
    a: f64,
    b: f64,
    c: Option<f64>,
    d: Option<f64>,
    time: f64,
) -> BirdInstantaneousVelocityResult {
    let dt: f64 = 1.0 / 60.0;
    let mut bird_positions: Vec<f64> = vec![];

    let correct_instantaneous_velocity: f64 = match function_type {
        "linear" => a,
        "quadratic" => (2.0 * a * time) + b,
        "cubic" => (3.0 * a * time.powi(2)) + (2.0 * b * time) + c.unwrap(),
        _ => unreachable!("Invalid function type")
    };
    let rounded_correct_instantaneous_velocity: f64 = (correct_instantaneous_velocity * 10.0).round() / 10.0;
    let student_instantaneous_velocity: f64 = (input_instantaneous_velocity * 10.0).round() / 10.0;

    let mut t: f64 = 0.0;
    while t <= time {
        let bird_position: f64 = match function_type {
            "linear" => (a * t) + b,
            "quadratic" => (a * t.powi(2)) + (b * t) + c.unwrap(),
            "cubic" => (a * t.powi(3)) + (b * t.powi(2)) + (c.unwrap() * t) + d.unwrap(),
            _ => unreachable!("Invalid function type")
        };

        bird_positions.push(bird_position);

        t += dt;
    }

    if student_instantaneous_velocity == rounded_correct_instantaneous_velocity {
        BirdInstantaneousVelocityResult{
            hit: true,
            correct_instantaneous_velocity: rounded_correct_instantaneous_velocity,
            bird_positions: bird_positions
        }
    } else {
        BirdInstantaneousVelocityResult{
            hit: false,
            correct_instantaneous_velocity: rounded_correct_instantaneous_velocity,
            bird_positions: bird_positions
        }
    }
}

#[pyfunction]
pub fn compute_bird_instantaneous_velocity(
    input_instantaneous_velocity: f64,
    function_type: &str,
    a: f64,
    b: f64,
    c: Option<f64>,
    d: Option<f64>,
    time: f64,
) -> PyResult<BirdInstantaneousVelocityResult> {
    Ok(compute_bird_instantaneous_velocity_logic(
        input_instantaneous_velocity,
        function_type,
        a,
        b,
        c,
        d,
        time
    ))
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_valid_compute_instantaneous_velocity_linear_logic() {
        const FUNCTION_TYPE: &str = "linear";
        const A: f64 = 9.0;
        const B: f64 = 5.5;
        const TIME: f64 = 5.5;

        let instantaneous_velocity_calculation: BirdInstantaneousVelocityResult = compute_bird_instantaneous_velocity_logic(
            9.0,
            FUNCTION_TYPE,
            A,
            B,
            None,
            None,
            TIME
        );

        assert!(instantaneous_velocity_calculation.hit);
        assert_eq!(instantaneous_velocity_calculation.correct_instantaneous_velocity, 9.0);
        assert!(instantaneous_velocity_calculation.bird_positions.len() > 0);
    }

    #[test]
    fn test_failed_compute_instantaneous_velocity_linear_logic() {
        const FUNCTION_TYPE: &str = "linear";
        const A: f64 = 9.0;
        const B: f64 = 5.5;
        const TIME: f64 = 5.5;

        let instantaneous_velocity_calculation: BirdInstantaneousVelocityResult = compute_bird_instantaneous_velocity_logic(
            8.0,
            FUNCTION_TYPE,
            A,
            B,
            None,
            None,
            TIME
        );

        assert!(!instantaneous_velocity_calculation.hit);
        assert_eq!(instantaneous_velocity_calculation.correct_instantaneous_velocity, 9.0);
    }

    #[test]
    fn test_valid_compute_instantaneous_velocity_quadratic_logic() {
        const FUNCTION_TYPE: &str = "quadratic";
        const A: f64 = 0.55;
        const B: f64 = 3.0;
        const C: f64 = 5.5;
        const TIME: f64 = 5.5;

        let instantaneous_velocity_calculation: BirdInstantaneousVelocityResult = compute_bird_instantaneous_velocity_logic(
            9.1,
            FUNCTION_TYPE,
            A,
            B,
            C,
            None,
            TIME
        );

        assert!(instantaneous_velocity_calculation.hit);
        assert_eq!(instantaneous_velocity_calculation.correct_instantaneous_velocity, 9.1);
        assert!(instantaneous_velocity_calculation.bird_positions.len() > 0);
    }

    #[test]
    fn test_failed_compute_instantaneous_velocity_quadratic_logic() {
        const FUNCTION_TYPE: &str = "quadratic";
        const A: f64 = 0.55;
        const B: f64 = 3.0;
        const C: f64 = 5.5;
        const TIME: f64 = 5.5;

        let instantaneous_velocity_calculation: BirdInstantaneousVelocityResult = compute_bird_instantaneous_velocity_logic(
            8.1,
            FUNCTION_TYPE,
            A,
            B,
            C,
            None,
            TIME
        );

        assert!(!instantaneous_velocity_calculation.hit);
        assert_eq!(instantaneous_velocity_calculation.correct_instantaneous_velocity, 9.1);
    }

    #[test]
    fn test_valid_compute_instantaneous_velocity_cubic_logic() {
        const FUNCTION_TYPE: &str = "cubic";
        const A: f64 = 0.0055;
        const B: f64 = 0.75;
        const C: f64 = 4.0;
        const D: f64 = 5.5;
        const TIME: f64 = 5.5;

        let instantaneous_velocity_calculation: BirdInstantaneousVelocityResult = compute_bird_instantaneous_velocity_logic(
            12.7,
            FUNCTION_TYPE,
            A,
            B,
            C,
            D,
            TIME
        );

        assert!(instantaneous_velocity_calculation.hit);
        assert_eq!(instantaneous_velocity_calculation.correct_instantaneous_velocity, 12.7);
        assert!(instantaneous_velocity_calculation.bird_positions.len() > 0);
    }

    #[test]
    fn test_failed_compute_instantaneous_velocity_cubic_logic() {
        const FUNCTION_TYPE: &str = "cubic";
        const A: f64 = 0.0055;
        const B: f64 = 0.75;
        const C: f64 = 4.0;
        const D: f64 = 5.5;
        const TIME: f64 = 5.5;

        let instantaneous_velocity_calculation: BirdInstantaneousVelocityResult = compute_bird_instantaneous_velocity_logic(
            11.7,
            FUNCTION_TYPE,
            A,
            B,
            C,
            D,
            TIME
        );

        assert!(!instantaneous_velocity_calculation.hit);
        assert_eq!(instantaneous_velocity_calculation.correct_instantaneous_velocity, 12.7);
    }
}