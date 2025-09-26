use chrono::{DateTime, NaiveDateTime, Utc};
use pyo3_polars::export::polars_core::prelude::PolarsError;
use std::collections::HashMap;
use once_cell::sync::Lazy;

/// Map of Carbonic format tokens to chrono format patterns
static CARBONIC_TOKEN_MAP: Lazy<HashMap<&'static str, &'static str>> = Lazy::new(|| {
    let mut map = HashMap::new();

    // Year tokens
    map.insert("Y", "%Y");      // 4-digit year
    map.insert("y", "%y");      // 2-digit year

    // Month tokens
    map.insert("m", "%m");      // Month with leading zero (01-12)
    map.insert("n", "%-m");     // Month without leading zero (1-12)
    map.insert("F", "%B");      // Full month name (localized)
    map.insert("M", "%b");      // Short month name (localized)

    // Day tokens
    map.insert("d", "%d");      // Day with leading zero (01-31)
    map.insert("j", "%-d");     // Day without leading zero (1-31)
    map.insert("l", "%A");      // Full day name (localized)
    map.insert("D", "%a");      // Short day name (localized)

    // Hour tokens
    map.insert("H", "%H");      // 24-hour with leading zero (00-23)
    map.insert("G", "%-H");     // 24-hour without leading zero (0-23)
    map.insert("h", "%I");      // 12-hour with leading zero (01-12)
    map.insert("g", "%-I");     // 12-hour without leading zero (1-12)

    // Minute/Second tokens
    map.insert("i", "%M");      // Minutes with leading zero (00-59)
    map.insert("s", "%S");      // Seconds with leading zero (00-59)

    // Microsecond/Millisecond tokens
    map.insert("u", "%f");      // Microseconds (000000-999999)
    map.insert("v", "%.3f");    // Milliseconds (000-999)

    // AM/PM tokens
    map.insert("A", "%p");      // AM/PM uppercase
    map.insert("a", "%P");      // am/pm lowercase

    // Timezone tokens
    map.insert("T", "%Z");      // Timezone abbreviation
    map.insert("P", "%z");      // Timezone offset (+0000)
    map.insert("O", "%z");      // Timezone offset (+0000)

    // Special format tokens
    map.insert("c", "%+");      // ISO 8601 format (2023-12-25T14:30:15+00:00)
    map.insert("r", "%a, %d %b %Y %H:%M:%S %z"); // RFC 2822

    map
});

/// Parse datetime string using Carbonic format tokens
pub fn parse_carbonic_format(
    input: &str,
    format: &str,
    _locale: &str,  // TODO: Use for localized month/day names
    strict: bool
) -> Result<DateTime<Utc>, PolarsError> {
    // Convert Carbonic format to chrono format
    let chrono_format = convert_carbonic_to_chrono_format(format)?;

    // Try parsing with chrono
    let result = if strict {
        // Strict mode: input must match format exactly
        NaiveDateTime::parse_from_str(input, &chrono_format)
            .map(|dt| dt.and_utc())
    } else {
        // Flexible mode: try common fallbacks
        parse_flexible(input, &chrono_format)
    };

    result.map_err(|e| PolarsError::ComputeError(
        format!("Failed to parse datetime '{}' with format '{}': {}", input, format, e).into()
    ))
}

/// Parse ISO 8601 datetime strings
pub fn parse_iso_8601(input: &str) -> Result<DateTime<Utc>, PolarsError> {
    // Try various ISO 8601 formats
    let formats = [
        "%Y-%m-%dT%H:%M:%S%.fZ",        // 2023-12-25T14:30:15.123Z
        "%Y-%m-%dT%H:%M:%SZ",           // 2023-12-25T14:30:15Z
        "%Y-%m-%dT%H:%M:%S%.f%z",       // 2023-12-25T14:30:15.123+0000
        "%Y-%m-%dT%H:%M:%S%z",          // 2023-12-25T14:30:15+0000
        "%Y-%m-%dT%H:%M:%S%.f",         // 2023-12-25T14:30:15.123 (naive)
        "%Y-%m-%dT%H:%M:%S",            // 2023-12-25T14:30:15 (naive)
        "%Y-%m-%d %H:%M:%S%.f",         // 2023-12-25 14:30:15.123 (space separator)
        "%Y-%m-%d %H:%M:%S",            // 2023-12-25 14:30:15
        "%Y-%m-%d",                     // 2023-12-25 (date only)
    ];

    for format in &formats {
        if let Ok(dt) = NaiveDateTime::parse_from_str(input, format) {
            return Ok(dt.and_utc());
        }
        if let Ok(dt) = DateTime::parse_from_str(input, format) {
            return Ok(dt.with_timezone(&Utc));
        }
    }

    Err(PolarsError::ComputeError(
        format!("Failed to parse ISO 8601 datetime: '{}'", input).into()
    ))
}

/// Convert Carbonic format tokens to chrono format
fn convert_carbonic_to_chrono_format(format: &str) -> Result<String, PolarsError> {
    let mut result = format.to_string();

    // Replace Carbonic tokens with chrono equivalents
    // Process longer tokens first to avoid conflicts
    let mut tokens: Vec<_> = CARBONIC_TOKEN_MAP.iter().collect();
    tokens.sort_by_key(|(k, _)| std::cmp::Reverse(k.len()));

    for (carbonic_token, chrono_token) in tokens {
        result = result.replace(carbonic_token, chrono_token);
    }

    Ok(result)
}

/// Flexible parsing with fallback formats
fn parse_flexible(input: &str, primary_format: &str) -> Result<DateTime<Utc>, chrono::ParseError> {
    // Try primary format first
    if let Ok(dt) = NaiveDateTime::parse_from_str(input, primary_format) {
        return Ok(dt.and_utc());
    }

    // Common fallback formats
    let fallback_formats = [
        "%Y-%m-%d %H:%M:%S",
        "%Y-%m-%d %H:%M",
        "%Y-%m-%d",
        "%d/%m/%Y %H:%M:%S",
        "%d/%m/%Y",
        "%m/%d/%Y %H:%M:%S",
        "%m/%d/%Y",
        "%d-%m-%Y %H:%M:%S",
        "%d-%m-%Y",
    ];

    for format in &fallback_formats {
        if let Ok(dt) = NaiveDateTime::parse_from_str(input, format) {
            return Ok(dt.and_utc());
        }
    }

    // Try with timezone-aware parsing
    let tz_formats = [
        "%Y-%m-%d %H:%M:%S %z",
        "%Y-%m-%d %H:%M:%S%z",
        "%Y-%m-%dT%H:%M:%S%z",
    ];

    for format in &tz_formats {
        if let Ok(dt) = DateTime::parse_from_str(input, format) {
            return Ok(dt.with_timezone(&Utc));
        }
    }

    // If no format worked, create a parse error by attempting an invalid parse
    NaiveDateTime::parse_from_str("", "%Y-%m-%d").map(|dt| dt.and_utc()).map_err(|e| e)
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_carbonic_format_conversion() {
        assert_eq!(
            convert_carbonic_to_chrono_format("Y-m-d H:i:s").unwrap(),
            "%Y-%m-%d %H:%M:%S"
        );

        assert_eq!(
            convert_carbonic_to_chrono_format("F j, Y").unwrap(),
            "%B %-d, %Y"
        );
    }

    #[test]
    fn test_parse_carbonic_format() {
        let result = parse_carbonic_format("2023-12-25 14:30:15", "Y-m-d H:i:s", "en", true);
        assert!(result.is_ok());

        let dt = result.unwrap();
        assert_eq!(dt.year(), 2023);
        assert_eq!(dt.month(), 12);
        assert_eq!(dt.day(), 25);
    }

    #[test]
    fn test_parse_iso_8601() {
        let inputs = [
            "2023-12-25T14:30:15Z",
            "2023-12-25T14:30:15.123Z",
            "2023-12-25T14:30:15+0000",
            "2023-12-25 14:30:15",
            "2023-12-25",
        ];

        for input in &inputs {
            let result = parse_iso_8601(input);
            assert!(result.is_ok(), "Failed to parse: {}", input);
        }
    }
}