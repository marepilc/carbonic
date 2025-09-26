use pyo3::prelude::*;
use pyo3_polars::PolarsAllocator;

pub mod expressions;
pub mod formatting;
pub mod parsing;
pub mod business_days;
pub mod utils;

#[global_allocator]
static ALLOC: PolarsAllocator = PolarsAllocator::new();

#[pymodule]
fn _internal(_py: Python, m: &PyModule) -> PyResult<()> {
    // Register parsing functions
    m.add_function(wrap_pyfunction!(expressions::parse_format, m)?)?;
    m.add_function(wrap_pyfunction!(expressions::parse_iso, m)?)?;

    // Register business day functions
    m.add_function(wrap_pyfunction!(expressions::add_business_days, m)?)?;
    m.add_function(wrap_pyfunction!(expressions::subtract_business_days, m)?)?;

    // Register formatting functions
    m.add_function(wrap_pyfunction!(expressions::format_localized, m)?)?;
    m.add_function(wrap_pyfunction!(expressions::humanize_duration, m)?)?;

    Ok(())
}