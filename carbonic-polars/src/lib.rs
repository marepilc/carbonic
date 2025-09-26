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
fn _internal(_m: &Bound<'_, PyModule>) -> PyResult<()> {
    Ok(())
}