# Changelog

All notable changes to Carbonic will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [1.0.2] - 2025-09-30

### 🔄 **Compatibility & Windows Support Release**

This release adds full Python standard library compatibility and Windows platform support.

#### Added

**Standard Library Compatibility**
- **`Date` ↔ `datetime.date` compatibility**: All properties and methods from `datetime.date` now available
  - Properties: `year`, `month`, `day`
  - Methods: `weekday()`, `isoweekday()`, `isoformat()`, `isocalendar()`, `timetuple()`, `toordinal()`, `replace()`
  - Direct comparisons with `datetime.date` objects now work
- **`DateTime` ↔ `datetime.datetime` compatibility**: Complete API parity with stdlib
  - Properties: `year`, `month`, `day`, `hour`, `minute`, `second`, `microsecond`, `tzinfo`, `fold`
  - Methods: `weekday()`, `isoweekday()`, `isoformat()`, `isocalendar()`, `date()`, `time()`, `timetz()`, `replace()`, `timetuple()`, `utctimetuple()`, `toordinal()`, `timestamp()`, `utcoffset()`, `dst()`, `tzname()`, `astimezone()`, `ctime()`
  - Direct comparisons with `datetime.datetime` objects now work
- **`Duration` ↔ `datetime.timedelta` compatibility**: Interoperability with stdlib timedelta
  - Property: `seconds` (matching timedelta API, in addition to existing `days` and `microseconds`)
  - Direct comparisons with `datetime.timedelta` objects now work (when no calendar components)

**Windows Platform Support**
- **Windows timezone support**: Added `tzdata` package as conditional dependency for Windows
  - Automatically installed on Windows via `platform_system == 'Windows'` marker
  - Resolves `ZoneInfoNotFoundError` on Windows systems
  - No impact on Unix/Linux systems which use OS-provided timezone data

**Parser Enhancements**
- **Microsecond support in ISO parsing**: Parser now handles `2024-01-15T14:30:45.123456Z` format
- **Space-separated datetime format**: Parser now supports `2024-01-15 14:30:45` format

#### Fixed
- **Windows timezone errors**: Fixed `ZoneInfoNotFoundError: 'No time zone found with key UTC'` on Windows
- **ISO datetime parsing**: Fixed parsing of ISO datetimes with microseconds
- **Documentation tests**: Fixed pydantic integration tests when pydantic not installed
- **Date.weekday property**: Changed from property to method to match `datetime.date` API

#### Changed
- **Breaking change**: `Date.weekday` is now a method `Date.weekday()` instead of a property (matches stdlib)
  - Update: `date.weekday` → `date.weekday()`
  - This aligns with Python's `datetime.date.weekday()` API
- **Comparison behavior**: `Date`, `DateTime`, and `Duration` can now be compared directly with stdlib equivalents
  - Previously: `Date(2024, 1, 15) != datetime.date(2024, 1, 15)` (different types)
  - Now: `Date(2024, 1, 15) == datetime.date(2024, 1, 15)` (True - compatible types)

#### Documentation
- **New compatibility guide**: Added comprehensive stdlib compatibility section to migration guide
- **Updated main docs**: Added "Standard Library Compatible" feature section to index
- **Updated examples**: All documentation examples updated to reflect new compatibility features

#### Examples

**Standard Library Compatibility**
```python
import datetime
from carbonic import Date, DateTime, Duration

# Date compatibility
carbonic_date = Date(2024, 1, 15)
native_date = datetime.date(2024, 1, 15)
assert carbonic_date == native_date  # True!
print(carbonic_date.weekday())       # 0 (Monday)

# DateTime compatibility
carbonic_dt = DateTime(2024, 1, 15, 14, 30, 45, tz="UTC")
native_dt = datetime.datetime(2024, 1, 15, 14, 30, 45, tzinfo=datetime.timezone.utc)
assert carbonic_dt == native_dt      # True!
print(carbonic_dt.timestamp())       # Works!

# Duration compatibility
carbonic_dur = Duration(days=1, hours=2)
native_td = datetime.timedelta(days=1, hours=2)
assert carbonic_dur == native_td     # True!

# Pass Carbonic objects to functions expecting stdlib types
def takes_date(d: datetime.date) -> str:
    return f"{d.year}-{d.month:02d}-{d.day:02d}"

result = takes_date(carbonic_date)   # Works seamlessly!
```

**Windows Support**
```python
# Now works on Windows without errors
from carbonic import now

current_time = now("UTC")  # Previously: ZoneInfoNotFoundError on Windows
print(current_time)        # Now works: 2024-01-15T14:30:45+00:00
```

#### Technical Details
- **Dependencies**: Added `tzdata>=2024.1` for Windows (`platform_system == 'Windows'`)
- **Test coverage**: All 432 tests pass on both Unix and Windows platforms
- **Type safety**: Full mypy compatibility maintained
- **Performance**: No performance impact; compatibility layer uses delegation
- **Backward compatibility**: All existing code continues to work (except `date.weekday` property → method)

#### Migration Notes

If you were using `Date.weekday` as a property:
```python
# Before (1.0.0-1.0.1)
if date.weekday == 0:  # Property access
    print("It's Monday!")

# After (1.0.2+)
if date.weekday() == 0:  # Method call (matches stdlib)
    print("It's Monday!")
```

This change brings Carbonic in line with Python's standard library `datetime.date.weekday()` method.

---

## [1.0.1] - 2025-09-28

### 🐛 **Bug Fix Release**

Critical timezone conversion functionality was missing from v1.0.0.

#### Added
- **`as_timezone()` method**: Convert DateTime objects between timezones with fluent API
- **Timezone conversion support**: Essential functionality for production timezone-aware applications

#### Fixed
- **Missing timezone conversion**: Users can now convert between timezones using `dt.as_timezone("America/New_York")`
- **Documentation gap**: Updated all examples to show proper timezone conversion usage
- **Fluent chaining**: Timezone conversion now integrates seamlessly with method chaining

#### Technical Details
- **New method**: `DateTime.as_timezone(tz: str | None) -> DateTime`
- **Comprehensive tests**: 12 new test cases covering DST transitions, edge cases, and error handling
- **Documentation updates**: Updated quickstart and guide with timezone conversion examples
- **Zero regressions**: All 483 tests pass, full type safety maintained

#### Examples
```python
# Convert between timezones
utc_time = DateTime.now()
ny_time = utc_time.as_timezone("America/New_York")
tokyo_time = utc_time.as_timezone("Asia/Tokyo")

# Fluent chaining with timezone conversion
result = (DateTime.now()
    .add(days=1)
    .start_of("day")
    .as_timezone("Europe/Warsaw")
    .format("Y-m-d H:i:s"))
```

This addresses the critical functionality gap identified in v1.0.0 documentation where timezone conversion was mentioned but not implemented.

---

## [1.0.0] - 2024-12-28

### 🎉 **First Major Release**

Carbonic v1.0.0 represents a complete, production-ready datetime library with comprehensive functionality, excellent developer experience, and robust internationalization support.

### 🏗️ **Core Foundation**

#### Added
- **5 Core Classes**: `DateTime`, `Date`, `Duration`, `Period`, `Interval`
- **Immutable Design**: All classes are frozen dataclasses with `__slots__` for memory efficiency
- **Type Safety**: Complete mypy compliance with PEP 561 support
- **Fluent API**: Method chaining with Pythonic naming conventions

### 📅 **Date & DateTime**

#### Added
- **Multiple Constructors**: `DateTime(year, month, day)`, `DateTime.now()`, `DateTime.today()`
- **ISO 8601 Parsing**: Strict and relaxed parsing with comprehensive error handling
- **Carbon-Style Formatting**: Flexible token-based formatting system
- **Format Documentation**: Complete reference tables in docstrings for IDE tooltips
- **Arithmetic Operations**: Full support for addition/subtraction with Duration
- **Anchor Methods**: `start_of()` and `end_of()` for periods (day, week, month, quarter, year)
- **Business Day Support**: `is_weekday()`, `is_weekend()`, `add_business_days()`
- **Timezone Support**: Full `zoneinfo` integration with proper UTC defaults
- **Comparison Operators**: Complete comparison support with timezone awareness

### ⏱️ **Duration**

#### Added
- **Flexible Construction**: Support for all time units including fractional values (`days=1.5`)
- **ISO 8601 Parsing**: Complete duration string parsing (`P1Y2M3DT4H5M6S`)
- **Human Readable**: Multi-language humanization ("2 hours 30 minutes")
- **Unit Conversions**: `in_days()`, `in_hours()`, etc. with `whole` parameter control
- **Calendar Components**: Proper handling of months and years
- **Arithmetic**: Full arithmetic and comparison operators

### 🌐 **Comprehensive Localization**

#### Added
- **6 Languages**: English, Polish, Spanish, French, German, Portuguese
- **Date/Time Formatting**: Localized month and day names
- **Duration Humanization**: Proper pluralization rules per language
- **Number Formatting**: Decimal comma support for European locales
- **Complex Grammar**: Polish 3-form pluralization (singular/plural/many)
- **Performance Optimized**: Lazy evaluation with caching for expensive operations
- **Extensible Architecture**: Clean design for adding new locales

### 🔗 **Framework Integration**

#### Added
- **Pydantic Integration**: Complete field types for validation and serialization
- **JSON Support**: Proper serialization/deserialization with type safety
- **Optional Dependencies**: Clean separation with `pip install carbonic[pydantic]`

### ⚡ **Performance**

#### Added
- **Fast Parsing**: Optional ciso8601 acceleration with graceful fallback
- **Memory Efficiency**: `__slots__` usage across all classes
- **Lazy Evaluation**: Cached expensive operations (locale lookups, timezone formatting)
- **Zero-Copy Operations**: Efficient immutable design patterns

### 🛠️ **Developer Experience**

#### Added
- **IDE Support**: Complete format token reference tables in docstrings
- **Type Annotations**: Precise overloads for excellent IntelliSense
- **Error Messages**: Clear, actionable error messages with context
- **Documentation**: Comprehensive API docs with practical examples
- **Fluent API**: Natural method chaining for readable code

### 📦 **Production Features**

#### Added
- **Relative Functions**: `today()`, `tomorrow()`, `yesterday()`, `next()`, `previous()`
- **Business Calendar**: Weekend detection and business day arithmetic
- **Interval Operations**: Time ranges with overlap, intersection, union
- **Period Constants**: Semantic time period operations (`Period.DAY`, `Period.WEEK`, etc.)
- **Exception Handling**: Custom exceptions with clear error contexts

### 🧪 **Quality Assurance**

#### Added
- **Comprehensive Testing**: 461 tests with edge case coverage
- **Type Safety**: Zero mypy errors across 19 source files
- **Code Quality**: All ruff linting checks pass
- **Documentation Tests**: All examples verified to work
- **Performance Tests**: Benchmarking for critical operations

### 🔧 **Technical Details**

#### Format Tokens
Complete Carbon-style formatting with comprehensive docstring reference:

**Date Tokens**: `Y`, `y`, `m`, `n`, `d`, `j`, `S`, `F`, `M`, `l`, `D`
**Time Tokens**: `H`, `G`, `h`, `g`, `i`, `s`, `A`, `a`, `u`, `v`
**Timezone Tokens**: `T`, `O`, `P`, `Z`
**Combined**: `c` (ISO 8601), `r` (RFC 2822)

#### Localization Details
- **English (en)**: Standard pluralization, decimal point
- **Polish (pl)**: Complex 3-form pluralization, decimal comma
- **Spanish (es)**: Standard pluralization, decimal comma
- **French (fr)**: Standard pluralization, decimal comma (mois invariant)
- **German (de)**: Standard pluralization, decimal comma
- **Portuguese (pt)**: Standard pluralization, decimal comma, compound day names

#### Dependencies
- **Required**: None (stdlib only)
- **Optional**:
  - `ciso8601>=2.3.0` for fast parsing
  - `pydantic>=2.0.0` for validation integration

### 📊 **Release Metrics**

- **5 Core Classes** with full functionality
- **6 Language Localizations** with proper grammar
- **461 Passing Tests** with comprehensive coverage
- **Zero Type Errors** with complete mypy compliance
- **19 Source Files** with production-ready quality

---

## Development Versions

### [0.2.2] - Development
- Pre-release development and testing

### [0.1.0] - Initial Development
- Initial project structure and core classes

---

**Legend:**
- 🎉 Major Release
- ✨ New Feature
- 🐛 Bug Fix
- 🔧 Technical Change
- 📚 Documentation
- 🔒 Security
- ⚠️ Breaking Change

[1.0.1]: https://github.com/marepilc/carbonic/releases/tag/v1.0.1
[1.0.0]: https://github.com/marepilc/carbonic/releases/tag/v1.0.0
[0.2.2]: https://github.com/marepilc/carbonic/compare/v0.1.0...v0.2.2
[0.1.0]: https://github.com/marepilc/carbonic/releases/tag/v0.1.0