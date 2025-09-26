use pyo3_polars::derive::polars_expr;
use pyo3_polars::export::polars_core::prelude::*;
use serde::Deserialize;

// Output type functions for polars_expr
fn datetime_output_type(_: &[Field]) -> PolarsResult<Field> {
    Ok(Field::new("datetime".into(), DataType::Datetime(TimeUnit::Microseconds, None)))
}

fn string_output_type(_: &[Field]) -> PolarsResult<Field> {
    Ok(Field::new("string".into(), DataType::String))
}

#[derive(Deserialize)]
struct ParseFormatKwargs {
    format: String,
    locale: Option<String>,
    strict: Option<bool>,
}

/// Parse datetime strings using Carbonic format tokens (placeholder implementation)
#[polars_expr(output_type_func=string_output_type)]
fn parse_format(inputs: &[Series], kwargs: ParseFormatKwargs) -> PolarsResult<Series> {
    let ca = inputs[0].str()?;
    let _format = kwargs.format;
    let _locale = kwargs.locale.unwrap_or_else(|| "en".to_string());
    let _strict = kwargs.strict.unwrap_or(false);

    // Placeholder: just return the input strings with a prefix
    let out = ca.apply_into_string_amortized(|value, output| {
        output.push_str("parsed:");
        output.push_str(value);
    });

    Ok(out.into_series())
}

/// Parse ISO 8601 datetime strings (placeholder implementation)
#[polars_expr(output_type_func=string_output_type)]
fn parse_iso(inputs: &[Series]) -> PolarsResult<Series> {
    let ca = inputs[0].str()?;

    // Placeholder: just return the input strings with a prefix
    let out = ca.apply_into_string_amortized(|value, output| {
        output.push_str("iso:");
        output.push_str(value);
    });

    Ok(out.into_series())
}