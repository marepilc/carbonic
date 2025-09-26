use chrono::{Datelike, NaiveDate, Weekday};
use polars::prelude::PolarsError;
use std::collections::HashSet;

/// Add business days to a date
pub fn add_bdays(
    date: i32,
    days: i32,
    weekends: &[String],
    holidays: &[String]
) -> Result<i32, PolarsError> {
    let start_date = days_to_naive_date(date)?;
    let weekend_set = parse_weekends(weekends)?;
    let holiday_set = parse_holidays(holidays)?;

    if days == 0 {
        return Ok(date);
    }

    let result_date = if days > 0 {
        add_business_days_forward(start_date, days as u32, &weekend_set, &holiday_set)
    } else {
        subtract_business_days_forward(start_date, (-days) as u32, &weekend_set, &holiday_set)
    };

    naive_date_to_days(result_date)
}

/// Subtract business days from a date
pub fn subtract_bdays(
    date: i32,
    days: i32,
    weekends: &[String],
    holidays: &[String]
) -> Result<i32, PolarsError> {
    add_bdays(date, -days, weekends, holidays)
}

/// Convert Polars date (days since epoch) to NaiveDate
fn days_to_naive_date(days: i32) -> Result<NaiveDate, PolarsError> {
    // Polars epoch is 1970-01-01
    NaiveDate::from_ymd_opt(1970, 1, 1)
        .ok_or_else(|| PolarsError::ComputeError("Invalid epoch date".into()))?
        .checked_add_signed(chrono::Duration::days(days as i64))
        .ok_or_else(|| PolarsError::ComputeError("Date overflow".into()))
}

/// Convert NaiveDate to Polars date (days since epoch)
fn naive_date_to_days(date: NaiveDate) -> Result<i32, PolarsError> {
    let epoch = NaiveDate::from_ymd_opt(1970, 1, 1)
        .ok_or_else(|| PolarsError::ComputeError("Invalid epoch date".into()))?;

    let duration = date.signed_duration_since(epoch);
    Ok(duration.num_days() as i32)
}

/// Parse weekend day names to Weekday set
fn parse_weekends(weekends: &[String]) -> Result<HashSet<Weekday>, PolarsError> {
    let mut weekend_set = HashSet::new();

    for day_str in weekends {
        let weekday = match day_str.to_lowercase().as_str() {
            "monday" | "mon" => Weekday::Mon,
            "tuesday" | "tue" => Weekday::Tue,
            "wednesday" | "wed" => Weekday::Wed,
            "thursday" | "thu" => Weekday::Thu,
            "friday" | "fri" => Weekday::Fri,
            "saturday" | "sat" => Weekday::Sat,
            "sunday" | "sun" => Weekday::Sun,
            _ => return Err(PolarsError::ComputeError(
                format!("Invalid weekday: '{}'", day_str).into()
            )),
        };
        weekend_set.insert(weekday);
    }

    Ok(weekend_set)
}

/// Parse holiday dates to NaiveDate set
fn parse_holidays(holidays: &[String]) -> Result<HashSet<NaiveDate>, PolarsError> {
    let mut holiday_set = HashSet::new();

    for holiday_str in holidays {
        // Try to parse as YYYY-MM-DD format
        let date = NaiveDate::parse_from_str(holiday_str, "%Y-%m-%d")
            .map_err(|_| PolarsError::ComputeError(
                format!("Invalid holiday date format '{}', expected YYYY-MM-DD", holiday_str).into()
            ))?;
        holiday_set.insert(date);
    }

    Ok(holiday_set)
}

/// Add business days forward
fn add_business_days_forward(
    mut date: NaiveDate,
    days: u32,
    weekends: &HashSet<Weekday>,
    holidays: &HashSet<NaiveDate>
) -> NaiveDate {
    let mut remaining_days = days;

    // Move to next business day if starting on weekend/holiday
    while is_non_business_day(date, weekends, holidays) {
        date = date.succ_opt().unwrap_or(date);
    }

    while remaining_days > 0 {
        date = date.succ_opt().unwrap_or(date);

        if !is_non_business_day(date, weekends, holidays) {
            remaining_days -= 1;
        }
    }

    date
}

/// Subtract business days (go backward)
fn subtract_business_days_forward(
    mut date: NaiveDate,
    days: u32,
    weekends: &HashSet<Weekday>,
    holidays: &HashSet<NaiveDate>
) -> NaiveDate {
    let mut remaining_days = days;

    // Move to previous business day if starting on weekend/holiday
    while is_non_business_day(date, weekends, holidays) {
        date = date.pred_opt().unwrap_or(date);
    }

    while remaining_days > 0 {
        date = date.pred_opt().unwrap_or(date);

        if !is_non_business_day(date, weekends, holidays) {
            remaining_days -= 1;
        }
    }

    date
}

/// Check if date is a non-business day (weekend or holiday)
fn is_non_business_day(
    date: NaiveDate,
    weekends: &HashSet<Weekday>,
    holidays: &HashSet<NaiveDate>
) -> bool {
    weekends.contains(&date.weekday()) || holidays.contains(&date)
}

#[cfg(test)]
mod tests {
    use super::*;
    use chrono::NaiveDate;

    #[test]
    fn test_add_business_days_simple() {
        // Monday 2023-12-25 + 1 business day = Tuesday 2023-12-26
        let monday = NaiveDate::from_ymd_opt(2023, 12, 25).unwrap();
        let monday_days = naive_date_to_days(monday).unwrap();

        let weekends = vec!["Saturday".to_string(), "Sunday".to_string()];
        let holidays = vec![];

        let result = add_bdays(monday_days, 1, &weekends, &holidays).unwrap();
        let result_date = days_to_naive_date(result).unwrap();

        assert_eq!(result_date, NaiveDate::from_ymd_opt(2023, 12, 26).unwrap());
    }

    #[test]
    fn test_add_business_days_skip_weekend() {
        // Friday 2023-12-22 + 1 business day = Monday 2023-12-25 (skip weekend)
        let friday = NaiveDate::from_ymd_opt(2023, 12, 22).unwrap();
        let friday_days = naive_date_to_days(friday).unwrap();

        let weekends = vec!["Saturday".to_string(), "Sunday".to_string()];
        let holidays = vec![];

        let result = add_bdays(friday_days, 1, &weekends, &holidays).unwrap();
        let result_date = days_to_naive_date(result).unwrap();

        assert_eq!(result_date, NaiveDate::from_ymd_opt(2023, 12, 25).unwrap());
    }

    #[test]
    fn test_add_business_days_with_holidays() {
        // Friday 2023-12-22 + 1 business day, but Monday is holiday = Tuesday 2023-12-26
        let friday = NaiveDate::from_ymd_opt(2023, 12, 22).unwrap();
        let friday_days = naive_date_to_days(friday).unwrap();

        let weekends = vec!["Saturday".to_string(), "Sunday".to_string()];
        let holidays = vec!["2023-12-25".to_string()]; // Christmas

        let result = add_bdays(friday_days, 1, &weekends, &holidays).unwrap();
        let result_date = days_to_naive_date(result).unwrap();

        assert_eq!(result_date, NaiveDate::from_ymd_opt(2023, 12, 26).unwrap());
    }

    #[test]
    fn test_subtract_business_days() {
        // Tuesday 2023-12-26 - 1 business day = Monday 2023-12-25
        let tuesday = NaiveDate::from_ymd_opt(2023, 12, 26).unwrap();
        let tuesday_days = naive_date_to_days(tuesday).unwrap();

        let weekends = vec!["Saturday".to_string(), "Sunday".to_string()];
        let holidays = vec![];

        let result = subtract_bdays(tuesday_days, 1, &weekends, &holidays).unwrap();
        let result_date = days_to_naive_date(result).unwrap();

        assert_eq!(result_date, NaiveDate::from_ymd_opt(2023, 12, 25).unwrap());
    }

    #[test]
    fn test_custom_weekends() {
        // Test with Friday-Saturday weekend (Middle East style)
        let thursday = NaiveDate::from_ymd_opt(2023, 12, 21).unwrap();
        let thursday_days = naive_date_to_days(thursday).unwrap();

        let weekends = vec!["Friday".to_string(), "Saturday".to_string()];
        let holidays = vec![];

        let result = add_bdays(thursday_days, 1, &weekends, &holidays).unwrap();
        let result_date = days_to_naive_date(result).unwrap();

        // Should skip Friday (weekend) and Saturday (weekend), land on Sunday
        assert_eq!(result_date, NaiveDate::from_ymd_opt(2023, 12, 24).unwrap());
    }

    #[test]
    fn test_parse_weekends() {
        let weekends = vec!["Saturday".to_string(), "Sunday".to_string()];
        let weekend_set = parse_weekends(&weekends).unwrap();

        assert!(weekend_set.contains(&Weekday::Sat));
        assert!(weekend_set.contains(&Weekday::Sun));
        assert!(!weekend_set.contains(&Weekday::Mon));
    }

    #[test]
    fn test_parse_holidays() {
        let holidays = vec!["2023-12-25".to_string(), "2024-01-01".to_string()];
        let holiday_set = parse_holidays(&holidays).unwrap();

        let christmas = NaiveDate::from_ymd_opt(2023, 12, 25).unwrap();
        let new_year = NaiveDate::from_ymd_opt(2024, 1, 1).unwrap();

        assert!(holiday_set.contains(&christmas));
        assert!(holiday_set.contains(&new_year));
    }
}