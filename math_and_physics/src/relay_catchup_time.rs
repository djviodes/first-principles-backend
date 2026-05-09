use pyo3::prelude::*;

#[pyclass]
pub struct RelayCatchupTimeResult {
    #[pyo3(get)]
    pub hit: bool,
    #[pyo3(get)]
    pub correct_catchup_time: f64,
    #[pyo3(get)]
    pub runner_one_positions: Vec<f64>,
    #[pyo3(get)]
    pub runner_two_positions: Vec<f64>,
}

fn compute_relay_catchup_time_logic(
    input_catchup_time: f64,
    a: f64,
    b_one: f64,
    b_two: f64,
    v_one: f64,
    v_two: f64,
    s_one: f64,
    s_two: f64
) -> RelayCatchupTimeResult {
    let dt: f64 = 1.0 / 60.0;
    let mut runner_one_positions: Vec<f64> = vec![];
    let mut runner_two_positions: Vec<f64> = vec![];

    let delta_b = b_one - b_two;
    let delta_v = v_one - v_two;
    let delta_s = s_one - s_two;

    let discriminant = delta_v.powi(2) - (2.0 * delta_b * delta_s);

    let time_one = (-delta_v + discriminant.sqrt()) / delta_b;
    let time_two = (-delta_v - discriminant.sqrt()) / delta_b;

    let correct_catchup_time: f64 = if time_one > 0.0 && time_two > 0.0 {
        time_one.min(time_two)
    } else if time_one > 0.0 {
        time_one
    } else if time_two > 0.0 {
        time_two
    } else {
        panic!("No positive solution found. Invalid inputs slipped through validation");
    };
    let rounded_correct_catchup_time: f64 = (correct_catchup_time * 10.0).round() / 10.0;
    let student_catchup_time: f64 = (input_catchup_time * 10.0).round() / 10.0;

    let mut t: f64 = 0.0;
    let mut vel_one = v_one;
    let mut vel_two = v_two;
    let mut pos_one = s_one;
    let mut pos_two = s_two;
    while t <= input_catchup_time {
        let acc_one = a * t + b_one;
        let acc_two = a * t + b_two;

        vel_one += acc_one * dt;
        vel_two += acc_two * dt;

        pos_one += vel_one * dt;
        pos_two += vel_two * dt;

        runner_one_positions.push(pos_one);
        runner_two_positions.push(pos_two);

        t += dt;
    }

    RelayCatchupTimeResult{
        hit: student_catchup_time == rounded_correct_catchup_time,
        correct_catchup_time: rounded_correct_catchup_time,
        runner_one_positions,
        runner_two_positions
    }
}

#[pyfunction]
pub fn compute_relay_catchup_time(
    input_catchup_time: f64,
    a: f64,
    b_one: f64,
    b_two: f64,
    v_one: f64,
    v_two: f64,
    s_one: f64,
    s_two: f64
) -> PyResult<RelayCatchupTimeResult> {
    Ok(compute_relay_catchup_time_logic(
        input_catchup_time,
        a,
        b_one,
        b_two,
        v_one,
        v_two,
        s_one,
        s_two,
    ))
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_valid_compute_relay_catchup_time_logic() {
        const A: f64 = 2.0;
        const B_ONE: f64 = 15.0;
        const B_TWO: f64 = 7.0;
        const V_ONE: f64 = 7.0;
        const V_TWO: f64 = 3.0;
        const S_ONE: f64 = 5.0;
        const S_TWO: f64 = 20.0;

        let catchup_time_calculation: RelayCatchupTimeResult = compute_relay_catchup_time_logic(
            1.5,
            A,
            B_ONE,
            B_TWO,
            V_ONE,
            V_TWO,
            S_ONE,
            S_TWO
        );

        assert!(catchup_time_calculation.hit);
        assert_eq!(catchup_time_calculation.correct_catchup_time, 1.5);
        assert!(catchup_time_calculation.runner_one_positions.len() > 0);
        assert!(catchup_time_calculation.runner_two_positions.len() > 0);
    }

    #[test]
    fn test_failed_compute_relay_catchup_time_logic() {
        const A: f64 = 2.0;
        const B_ONE: f64 = 15.0;
        const B_TWO: f64 = 7.0;
        const V_ONE: f64 = 7.0;
        const V_TWO: f64 = 3.0;
        const S_ONE: f64 = 5.0;
        const S_TWO: f64 = 20.0;

        let catchup_time_calculation: RelayCatchupTimeResult = compute_relay_catchup_time_logic(
            2.0,
            A,
            B_ONE,
            B_TWO,
            V_ONE,
            V_TWO,
            S_ONE,
            S_TWO
        );

        assert!(!catchup_time_calculation.hit);
        assert_eq!(catchup_time_calculation.correct_catchup_time, 1.5);
        assert!(catchup_time_calculation.runner_one_positions.len() > 0);
        assert!(catchup_time_calculation.runner_two_positions.len() > 0);
    }
}