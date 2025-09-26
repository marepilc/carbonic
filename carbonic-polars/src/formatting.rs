use chrono::{DateTime, Utc, Timelike, Datelike};
use std::collections::HashMap;
use once_cell::sync::Lazy;

/// Localized month names
static MONTH_NAMES: Lazy<HashMap<&'static str, [&'static str; 12]>> = Lazy::new(|| {
    let mut map = HashMap::new();

    map.insert("en", [
        "January", "February", "March", "April", "May", "June",
        "July", "August", "September", "October", "November", "December"
    ]);

    map.insert("pl", [
        "styczeń", "luty", "marzec", "kwiecień", "maj", "czerwiec",
        "lipiec", "sierpień", "wrzesień", "październik", "listopad", "grudzień"
    ]);

    map
});

/// Localized short month names
static SHORT_MONTH_NAMES: Lazy<HashMap<&'static str, [&'static str; 12]>> = Lazy::new(|| {
    let mut map = HashMap::new();

    map.insert("en", [
        "Jan", "Feb", "Mar", "Apr", "May", "Jun",
        "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"
    ]);

    map.insert("pl", [
        "sty", "lut", "mar", "kwi", "maj", "cze",
        "lip", "sie", "wrz", "paź", "lis", "gru"
    ]);

    map
});

/// Localized day names
static DAY_NAMES: Lazy<HashMap<&'static str, [&'static str; 7]>> = Lazy::new(|| {
    let mut map = HashMap::new();

    map.insert("en", [
        "Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"
    ]);

    map.insert("pl", [
        "poniedziałek", "wtorek", "środa", "czwartek", "piątek", "sobota", "niedziela"
    ]);

    map
});

/// Localized short day names
static SHORT_DAY_NAMES: Lazy<HashMap<&'static str, [&'static str; 7]>> = Lazy::new(|| {
    let mut map = HashMap::new();

    map.insert("en", [
        "Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"
    ]);

    map.insert("pl", [
        "pon", "wto", "śro", "czw", "pią", "sob", "nie"
    ]);

    map
});

/// Format timestamp with localized output
pub fn format_with_locale(
    timestamp_micros: i64,
    format: &str,
    locale: &str,
    output: &mut String
) {
    // Convert microseconds to DateTime
    let secs = timestamp_micros / 1_000_000;
    let nanos = ((timestamp_micros % 1_000_000) * 1000) as u32;

    let datetime = match DateTime::from_timestamp(secs, nanos) {
        Some(dt) => dt,
        None => {
            output.push_str("Invalid datetime");
            return;
        }
    };

    // Process format tokens
    let result = process_format_tokens(datetime, format, locale);
    output.push_str(&result);
}

/// Process Carbonic format tokens with localization
fn process_format_tokens(datetime: DateTime<Utc>, format: &str, locale: &str) -> String {
    let mut result = String::with_capacity(format.len() * 2);
    let mut chars = format.chars().peekable();

    while let Some(ch) = chars.next() {
        match ch {
            // Escape sequences
            '\\' => {
                if let Some(&next_ch) = chars.peek() {
                    chars.next();
                    result.push(next_ch);
                } else {
                    result.push('\\');
                }
            }
            // Year tokens
            'Y' => result.push_str(&format!("{:04}", datetime.year())),
            'y' => result.push_str(&format!("{:02}", datetime.year() % 100)),

            // Month tokens
            'm' => result.push_str(&format!("{:02}", datetime.month())),
            'n' => result.push_str(&datetime.month().to_string()),
            'F' => {
                let month_name = get_month_name(datetime.month() as usize - 1, false, locale);
                result.push_str(month_name);
            }
            'M' => {
                let month_name = get_month_name(datetime.month() as usize - 1, true, locale);
                result.push_str(month_name);
            }

            // Day tokens
            'd' => result.push_str(&format!("{:02}", datetime.day())),
            'j' => result.push_str(&datetime.day().to_string()),
            'l' => {
                let day_name = get_day_name(datetime.weekday().num_days_from_monday() as usize, false, locale);
                result.push_str(day_name);
            }
            'D' => {
                let day_name = get_day_name(datetime.weekday().num_days_from_monday() as usize, true, locale);
                result.push_str(day_name);
            }

            // Hour tokens
            'H' => result.push_str(&format!("{:02}", datetime.hour())),
            'G' => result.push_str(&datetime.hour().to_string()),
            'h' => {
                let hour_12 = match datetime.hour() {
                    0 => 12,
                    h if h > 12 => h - 12,
                    h => h,
                };
                result.push_str(&format!("{:02}", hour_12));
            }
            'g' => {
                let hour_12 = match datetime.hour() {
                    0 => 12,
                    h if h > 12 => h - 12,
                    h => h,
                };
                result.push_str(&hour_12.to_string());
            }

            // Minute/Second tokens
            'i' => result.push_str(&format!("{:02}", datetime.minute())),
            's' => result.push_str(&format!("{:02}", datetime.second())),

            // Microsecond tokens
            'u' => result.push_str(&format!("{:06}", datetime.timestamp_subsec_micros())),
            'v' => result.push_str(&format!("{:03}", datetime.timestamp_subsec_millis())),

            // AM/PM tokens
            'A' => result.push_str(if datetime.hour() < 12 { "AM" } else { "PM" }),
            'a' => result.push_str(if datetime.hour() < 12 { "am" } else { "pm" }),

            // Special formats
            'c' => result.push_str(&datetime.to_rfc3339()),
            'r' => result.push_str(&datetime.format("%a, %d %b %Y %H:%M:%S %z").to_string()),

            // Literal character
            _ => result.push(ch),
        }
    }

    result
}

/// Get localized month name
fn get_month_name(month_index: usize, short: bool, locale: &str) -> &'static str {
    let names = if short {
        SHORT_MONTH_NAMES.get(locale).unwrap_or(&SHORT_MONTH_NAMES["en"])
    } else {
        MONTH_NAMES.get(locale).unwrap_or(&MONTH_NAMES["en"])
    };

    names.get(month_index).unwrap_or(&names[0])
}

/// Get localized day name
fn get_day_name(day_index: usize, short: bool, locale: &str) -> &'static str {
    let names = if short {
        SHORT_DAY_NAMES.get(locale).unwrap_or(&SHORT_DAY_NAMES["en"])
    } else {
        DAY_NAMES.get(locale).unwrap_or(&DAY_NAMES["en"])
    };

    names.get(day_index).unwrap_or(&names[0])
}

/// Humanize duration with localization
pub fn humanize_duration_str(
    duration_secs: f64,
    locale: &str,
    max_units: i32,
    output: &mut String
) {
    if duration_secs == 0.0 {
        output.push_str(&get_duration_unit_name("second", 0, locale));
        return;
    }

    let is_negative = duration_secs < 0.0;
    let abs_duration = duration_secs.abs();

    // Calculate units
    let years = (abs_duration / (365.25 * 24.0 * 3600.0)) as i32;
    let remaining_after_years = abs_duration % (365.25 * 24.0 * 3600.0);

    let months = (remaining_after_years / (30.44 * 24.0 * 3600.0)) as i32;
    let remaining_after_months = remaining_after_years % (30.44 * 24.0 * 3600.0);

    let days = (remaining_after_months / (24.0 * 3600.0)) as i32;
    let remaining_after_days = remaining_after_months % (24.0 * 3600.0);

    let hours = (remaining_after_days / 3600.0) as i32;
    let remaining_after_hours = remaining_after_days % 3600.0;

    let minutes = (remaining_after_hours / 60.0) as i32;
    let seconds = remaining_after_hours % 60.0;

    // Build parts array
    let mut parts = Vec::new();

    if years > 0 { parts.push((years, "year")); }
    if months > 0 { parts.push((months, "month")); }
    if days > 0 { parts.push((days, "day")); }
    if hours > 0 { parts.push((hours, "hour")); }
    if minutes > 0 { parts.push((minutes, "minute")); }
    if seconds > 0.0 || parts.is_empty() {
        if seconds.fract() == 0.0 {
            parts.push((seconds as i32, "second"));
        } else {
            // Handle fractional seconds
            let formatted_seconds = if locale == "pl" {
                format!("{:.3}", seconds).replace('.', ",")
            } else {
                format!("{:.3}", seconds)
            };
            output.push_str(&format!("{}{} {}",
                if is_negative { "-" } else { "" },
                formatted_seconds,
                get_duration_unit_name("second", if seconds < 2.0 { 1 } else { 2 }, locale)
            ));
            return;
        }
    }

    // Take only max_units
    parts.truncate(max_units as usize);

    // Format output
    if is_negative {
        output.push('-');
    }

    let formatted_parts: Vec<String> = parts.into_iter()
        .map(|(count, unit)| {
            format!("{} {}", count, get_duration_unit_name(unit, count, locale))
        })
        .collect();

    output.push_str(&formatted_parts.join(" "));
}

/// Get localized duration unit name with proper pluralization
fn get_duration_unit_name(unit: &str, count: i32, locale: &str) -> &'static str {
    match locale {
        "pl" => get_polish_duration_unit(unit, count),
        _ => get_english_duration_unit(unit, count),
    }
}

/// Get English duration unit name
fn get_english_duration_unit(unit: &str, count: i32) -> &'static str {
    match unit {
        "year" => if count == 1 { "year" } else { "years" },
        "month" => if count == 1 { "month" } else { "months" },
        "day" => if count == 1 { "day" } else { "days" },
        "hour" => if count == 1 { "hour" } else { "hours" },
        "minute" => if count == 1 { "minute" } else { "minutes" },
        "second" => if count == 1 { "second" } else { "seconds" },
        _ => "unknown",
    }
}

/// Get Polish duration unit name with complex pluralization
fn get_polish_duration_unit(unit: &str, count: i32) -> &'static str {
    let abs_count = count.abs();

    // Polish pluralization rules
    let form = if abs_count == 1 {
        0 // singular
    } else if (abs_count % 100 >= 12 && abs_count % 100 <= 14) ||
              (abs_count % 10 == 0 || abs_count % 10 >= 5) {
        2 // many
    } else {
        1 // plural (2-4)
    };

    match unit {
        "year" => ["rok", "lata", "lat"][form],
        "month" => ["miesiąc", "miesiące", "miesięcy"][form],
        "day" => ["dzień", "dni", "dni"][form],
        "hour" => ["godzina", "godziny", "godzin"][form],
        "minute" => ["minuta", "minuty", "minut"][form],
        "second" => ["sekunda", "sekundy", "sekund"][form],
        _ => "nieznane",
    }
}

#[cfg(test)]
mod tests {
    use super::*;
    use chrono::{DateTime, Utc};

    #[test]
    fn test_format_with_locale_english() {
        // 2023-12-25 14:30:15 UTC
        let timestamp = 1703516215_000_000i64; // microseconds
        let mut output = String::new();

        format_with_locale(timestamp, "F j, Y", "en", &mut output);
        assert_eq!(output, "December 25, 2023");
    }

    #[test]
    fn test_format_with_locale_polish() {
        // 2023-12-25 14:30:15 UTC
        let timestamp = 1703516215_000_000i64; // microseconds
        let mut output = String::new();

        format_with_locale(timestamp, "F j, Y", "pl", &mut output);
        assert_eq!(output, "grudzień 25, 2023");
    }

    #[test]
    fn test_humanize_duration_english() {
        let mut output = String::new();
        humanize_duration_str(3661.0, "en", 2, &mut output); // 1h 1m 1s
        assert_eq!(output, "1 hour 1 minute");
    }

    #[test]
    fn test_humanize_duration_polish() {
        let mut output = String::new();
        humanize_duration_str(7200.0, "pl", 1, &mut output); // 2 hours
        assert_eq!(output, "2 godziny");
    }

    #[test]
    fn test_polish_pluralization() {
        // Test various Polish pluralization cases
        assert_eq!(get_polish_duration_unit("day", 1), "dzień");     // singular
        assert_eq!(get_polish_duration_unit("day", 2), "dni");      // plural
        assert_eq!(get_polish_duration_unit("day", 5), "dni");      // many
        assert_eq!(get_polish_duration_unit("day", 12), "dni");     // teens (many)
        assert_eq!(get_polish_duration_unit("day", 22), "dni");     // 22 (plural)
    }
}