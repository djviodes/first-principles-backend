use pyo3::prelude::*;

#[pyclass]
pub struct SquirrelPartAResult {
    #[pyo3(get)]
    pub hit: bool,
    #[pyo3(get)]
    pub correct_a_x: f64,
    #[pyo3(get)]
    pub correct_b_x: f64,
    #[pyo3(get)]
    pub correct_c_y: f64,
    #[pyo3(get)]
    pub squirrel_x_positions: Vec<f64>,
    #[pyo3(get)]
    pub squirrel_y_positions: Vec<f64>,
}

#[pyclass]
pub struct SquirrelPartBResult {
    #[pyo3(get)]
    pub hit: bool,
    #[pyo3(get)]
    pub correct_distance: f64,
}

#[pyclass]
pub struct SquirrelPartCResult {
    #[pyo3(get)]
    pub hit: bool,
    #[pyo3(get)]
    pub correct_magnitude: f64,
    #[pyo3(get)]
    pub correct_direction: f64,
}

fn compute_squirrel_part_a_logic(
    input_a_x: f64,
    input_b_x: f64,
    input_c_y: f64,
    a_x: f64,
    b_x: f64,
    c_y: f64,
    time: f64
) -> SquirrelPartAResult {
    let dt: f64 = 1.0 / 60.0;
    let mut squirrel_x_positions: Vec<f64> = vec![];
    let mut squirrel_y_positions: Vec<f64> = vec![];

    let correct_a_x: f64 = a_x;
    let correct_b_x: f64 = 2.0 * b_x;
    let correct_c_y: f64 = 3.0 * c_y;
    let rounded_correct_a_x: f64 = (correct_a_x * 1000.0).round() / 1000.0;
    let rounded_correct_b_x: f64 = (correct_b_x * 1000.0).round() / 1000.0;
    let rounded_correct_c_y: f64 = (correct_c_y * 1000.0).round() / 1000.0;
    let student_a_x: f64 = (input_a_x * 1000.0).round() / 1000.0;
    let student_b_x: f64 = (input_b_x * 1000.0).round() / 1000.0;
    let student_c_y: f64 = (input_c_y * 1000.0).round() / 1000.0;

    let mut t: f64 = 0.0;
    while t <= time {
        let x_position: f64 = (input_a_x * t) + (input_b_x * t.powi(2));
        let y_position: f64 = input_c_y * t.powi(3);

        squirrel_x_positions.push(x_position);
        squirrel_y_positions.push(y_position);

        t += dt;
    }

    SquirrelPartAResult{
        hit: (
            student_a_x == rounded_correct_a_x
            && student_b_x == rounded_correct_b_x
            && student_c_y == rounded_correct_c_y
        ),
        correct_a_x: rounded_correct_a_x,
        correct_b_x: rounded_correct_b_x,
        correct_c_y: rounded_correct_c_y,
        squirrel_x_positions,
        squirrel_y_positions
    }
}

fn compute_squirrel_part_b_logic(
    input_distance: f64,
    a_x: f64,
    b_x: f64,
    c_y: f64,
    time: f64
) -> SquirrelPartBResult {
    let correct_distance: f64 = (
        ((a_x * time) + (b_x * time.powi(2))).powi(2)
        + (c_y * time.powi(3)).powi(2)
    ).sqrt();
    let rounded_correct_distance: f64 = (correct_distance * 1000.0).round() / 1000.0;
    let student_distance: f64 = (input_distance * 1000.0).round() / 1000.0;

    SquirrelPartBResult{
        hit: student_distance == rounded_correct_distance,
        correct_distance: rounded_correct_distance
    }
}

fn compute_squirrel_part_c_logic(
    input_magnitude: f64,
    input_direction: f64,
    a_x: f64,
    b_x: f64,
    c_y: f64,
    time: f64
) -> SquirrelPartCResult {
    let correct_magnitude: f64 = (
        (a_x + (2.0 * b_x * time)).powi(2)
        + (3.0 * c_y * time.powi(2)).powi(2)
    ).sqrt();
    let correct_direction: f64 = (
        (3.0 * c_y * time.powi(2))
        / (a_x + (2.0 * b_x * time))
    ).atan().to_degrees();
    let rounded_correct_magnitude: f64 = (correct_magnitude * 1000.0).round() / 1000.0;
    let rounded_correct_direction: f64 = (correct_direction * 1000.0).round() / 1000.0;
    let student_magnitude: f64 = (input_magnitude * 1000.0).round() / 1000.0;
    let student_direction: f64 = (input_direction * 1000.0).round() / 1000.0;

    SquirrelPartCResult{
        hit: (
            student_magnitude == rounded_correct_magnitude
            && student_direction == rounded_correct_direction
        ),
        correct_magnitude: rounded_correct_magnitude,
        correct_direction: rounded_correct_direction
    }
}

#[pyfunction]
pub fn compute_squirrel_part_a(
    input_a_x: f64,
    input_b_x: f64,
    input_c_y: f64,
    a_x: f64,
    b_x: f64,
    c_y: f64,
    time: f64
) -> PyResult<SquirrelPartAResult> {
    Ok(compute_squirrel_part_a_logic(
        input_a_x,
        input_b_x,
        input_c_y,
        a_x,
        b_x,
        c_y,
        time
    ))
}

#[pyfunction]
pub fn compute_squirrel_part_b(
    input_distance: f64,
    a_x: f64,
    b_x: f64,
    c_y: f64,
    time: f64
) -> PyResult<SquirrelPartBResult> {
    Ok(compute_squirrel_part_b_logic(
        input_distance,
        a_x,
        b_x,
        c_y,
        time
    ))
}

#[pyfunction]
pub fn compute_squirrel_part_c(
    input_magnitude: f64,
    input_direction: f64,
    a_x: f64,
    b_x: f64,
    c_y: f64,
    time: f64
) -> PyResult<SquirrelPartCResult> {
    Ok(compute_squirrel_part_c_logic(
        input_magnitude,
        input_direction,
        a_x,
        b_x,
        c_y,
        time
    ))
}