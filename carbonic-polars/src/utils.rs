/// Utility functions for the Carbonic Polars plugin

use chrono::{DateTime, Utc, NaiveDate};
use pyo3_polars::export::polars_core::prelude::PolarsError;

/// Convert various datetime representations to microseconds since Unix epoch
pub fn to_timestamp_micros(year: i32, month: u32, day: u32, hour: u32, minute: u32, second: u32, microsecond: u32) -> Result<i64, PolarsError> {
    let naive = NaiveDate::from_ymd_opt(year, month, day)
        .and_then(|d| d.and_hms_micro_opt(hour, minute, second, microsecond))
        .ok_or_else(|| PolarsError::ComputeError("Invalid datetime components".into()))?;

    Ok(naive.and_utc().timestamp_micros())
}

/// Convert microseconds since Unix epoch to DateTime<Utc>
pub fn from_timestamp_micros(timestamp_micros: i64) -> Result<DateTime<Utc>, PolarsError> {
    let secs = timestamp_micros / 1_000_000;
    let nanos = ((timestamp_micros % 1_000_000) * 1000) as u32;

    DateTime::from_timestamp(secs, nanos)
        .ok_or_else(|| PolarsError::ComputeError("Invalid timestamp".into()))
}

/// Validate that a format string contains only supported tokens
pub fn validate_format_string(format: &str) -> Result<(), PolarsError> {
    let supported_tokens = [
        "Y", "y",           // Year
        "m", "n", "F", "M", // Month
        "d", "j", "l", "D", // Day
        "H", "G", "h", "g", // Hour
        "i", "s",           // Minute/Second
        "u", "v",           // Microsecond/Millisecond
        "A", "a",           // AM/PM
        "T", "P", "O",      // Timezone
        "c", "r",           // Special formats
    ];

    // Simple validation - check for unknown single-char tokens
    // This is a basic check; more sophisticated validation could be added
    for ch in format.chars() {
        if ch.is_alphabetic() && !supported_tokens.contains(&ch.to_string().as_str()) {
            // Allow common literal characters and escapes
            if !"\\-/:.,; ()[]{}".contains(ch) {
                return Err(PolarsError::ComputeError(
                    format!("Unsupported format token: '{}'", ch).into()
                ));
            }
        }
    }

    Ok(())
}

/// Helper to safely handle null values in Series operations
#[inline]
pub fn handle_null_propagation<T, F>(opt_value: Option<T>, operation: F) -> Option<T>
where
    F: FnOnce(T) -> Option<T>,
{
    match opt_value {
        Some(value) => operation(value),
        None => None,
    }
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_timestamp_conversion() {
        let timestamp = to_timestamp_micros(2023, 12, 25, 14, 30, 15, 123456).unwrap();
        let datetime = from_timestamp_micros(timestamp).unwrap();

        assert_eq!(datetime.year(), 2023);
        assert_eq!(datetime.month(), 12);
        assert_eq!(datetime.day(), 25);
        assert_eq!(datetime.hour(), 14);
        assert_eq!(datetime.minute(), 30);
        assert_eq!(datetime.second(), 15);
        assert_eq!(datetime.timestamp_subsec_micros(), 123456);
    }

    #[test]
    fn test_format_validation() {
        assert!(validate_format_string("Y-m-d H:i:s").is_ok());
        assert!(validate_format_string("F j, Y").is_ok());
        assert!(validate_format_string("c").is_ok());

        // Invalid token should fail
        assert!(validate_format_string("Y-m-d Q").is_err());
    }

    #[test]
    fn test_null_propagation() {
        let result = handle_null_propagation(Some(42), |x| Some(x * 2));
        assert_eq!(result, Some(84));

        let result = handle_null_propagation(None::<i32>, |x| Some(x * 2));
        assert_eq!(result, None);
    }
}