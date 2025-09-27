# Changelog

All notable changes to Carbonic will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

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

[1.0.0]: https://github.com/marepilc/carbonic/releases/tag/v1.0.0
[0.2.2]: https://github.com/marepilc/carbonic/compare/v0.1.0...v0.2.2
[0.1.0]: https://github.com/marepilc/carbonic/releases/tag/v0.1.0