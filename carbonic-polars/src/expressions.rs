use polars::prelude::*;
use pyo3_polars::derive::polars_expr;
use serde::Deserialize;

use crate::parsing::{parse_carbonic_format, parse_iso_8601};
use crate::business_days::{add_bdays, subtract_bdays};
use crate::formatting::{format_with_locale, humanize_duration_str};

#[derive(Deserialize)]
struct ParseFormatKwargs {
    format: String,
    locale: Option<String>,
    strict: Option<bool>,
}

#[derive(Deserialize)]
struct BusinessDayKwargs {
    weekends: Option<Vec<String>>,
    holidays: Option<Vec<String>>,
}

#[derive(Deserialize)]
struct FormatKwargs {
    format: String,
    locale: Option<String>,
}

#[derive(Deserialize)]
struct HumanizeKwargs {
    locale: Option<String>,
    max_units: Option<i32>,
}

/// Parse datetime strings using Carbonic format tokens
#[polars_expr(output_type=Datetime(TimeUnit::Microseconds, None))]
fn parse_format(inputs: &[Series], kwargs: ParseFormatKwargs) -> PolarsResult<Series> {
    let ca = inputs[0].str()?;
    let format = kwargs.format;
    let locale = kwargs.locale.unwrap_or_else(|| "en".to_string());
    let strict = kwargs.strict.unwrap_or(false);

    let out: DatetimeChunked = ca.apply_nonnull_values_generic(
        DataType::Datetime(TimeUnit::Microseconds, None),
        |s| {
            parse_carbonic_format(s, &format, &locale, strict)
                .map(|dt| dt.timestamp_micros())
        }
    );

    Ok(out.into_series())
}

/// Parse ISO 8601 datetime strings
#[polars_expr(output_type=Datetime(TimeUnit::Microseconds, None))]
fn parse_iso(inputs: &[Series]) -> PolarsResult<Series> {
    let ca = inputs[0].str()?;

    let out: DatetimeChunked = ca.apply_nonnull_values_generic(
        DataType::Datetime(TimeUnit::Microseconds, None),
        |s| {
            parse_iso_8601(s)
                .map(|dt| dt.timestamp_micros())
        }
    );

    Ok(out.into_series())
}

/// Add business days to dates
#[polars_expr(output_type=Date)]
fn add_business_days(inputs: &[Series], kwargs: BusinessDayKwargs) -> PolarsResult<Series> {
    let dates = inputs[0].date()?;
    let days = inputs[1].i32()?;

    let weekends = kwargs.weekends.unwrap_or_else(|| vec!["Saturday".to_string(), "Sunday".to_string()]);
    let holidays = kwargs.holidays.unwrap_or_default();

    let out: DateChunked = dates
        .zip_with(&days, |date_opt, days_opt| {
            match (date_opt, days_opt) {
                (Some(date), Some(days)) => {
                    add_bdays(date, days, &weekends, &holidays).ok()
                },
                _ => None,
            }
        })?;

    Ok(out.into_series())
}

/// Subtract business days from dates
#[polars_expr(output_type=Date)]
fn subtract_business_days(inputs: &[Series], kwargs: BusinessDayKwargs) -> PolarsResult<Series> {
    let dates = inputs[0].date()?;
    let days = inputs[1].i32()?;

    let weekends = kwargs.weekends.unwrap_or_else(|| vec!["Saturday".to_string(), "Sunday".to_string()]);
    let holidays = kwargs.holidays.unwrap_or_default();

    let out: DateChunked = dates
        .zip_with(&days, |date_opt, days_opt| {
            match (date_opt, days_opt) {
                (Some(date), Some(days)) => {
                    subtract_bdays(date, days, &weekends, &holidays).ok()
                },
                _ => None,
            }
        })?;

    Ok(out.into_series())
}

/// Format datetime with localized output
#[polars_expr(output_type=String)]
fn format_localized(inputs: &[Series], kwargs: FormatKwargs) -> PolarsResult<Series> {
    let ca = inputs[0].datetime()?;
    let format = kwargs.format;
    let locale = kwargs.locale.unwrap_or_else(|| "en".to_string());

    let out: StringChunked = ca.apply_into_string_amortized(|timestamp_opt, output| {
        match timestamp_opt {
            Some(timestamp) => {
                format_with_locale(timestamp, &format, &locale, output)
            },
            None => output.push_str(""),
        }
    });

    Ok(out.into_series())
}

/// Humanize duration with localization
#[polars_expr(output_type=String)]
fn humanize_duration(inputs: &[Series], kwargs: HumanizeKwargs) -> PolarsResult<Series> {
    let ca = inputs[0].duration()?;
    let locale = kwargs.locale.unwrap_or_else(|| "en".to_string());
    let max_units = kwargs.max_units.unwrap_or(2);

    let out: StringChunked = ca.apply_into_string_amortized(|duration_opt, output| {
        match duration_opt {
            Some(duration_ns) => {
                let duration_secs = duration_ns as f64 / 1_000_000_000.0;
                humanize_duration_str(duration_secs, &locale, max_units, output)
            },
            None => output.push_str(""),
        }
    });

    Ok(out.into_series())
}