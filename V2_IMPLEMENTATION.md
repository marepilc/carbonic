# Carbonic 2.0 Implementation Tracker

This file is the working source of truth for the Carbonic 2.0 rewrite.

It tracks:
- decisions that are already locked
- work that is done
- work that is next
- work that is intentionally deferred

## 1. Locked Decisions

### API and type model

- `Date` must be a native subtype of `datetime.date`
- `DateTime` must be a native subtype of `datetime.datetime`
- The wrapper model from 1.x is not acceptable for 2.0
- Static typing must allow:

```python
import datetime

from carbonic import Date, DateTime

d: datetime.date = Date(2026, 4, 24)
dt: datetime.datetime = DateTime(2026, 4, 24, 12, 0, tz="UTC")
```

### Formatting and parsing

- Carbon-style formatting tokens will be removed
- Public formatting should be Pythonic only:
  - `strftime`
  - `strptime`
  - `isoformat`
  - `fromisoformat`
- Parsing should be strict by default
- Ambiguous automatic parsing should be avoided or removed
- Cross-platform behavior must be explicit, especially for Windows-incompatible `strftime` directives such as `%-d`

### Documentation

- Current documentation is considered disposable
- MkDocs/Material should not drive 2.0 design decisions
- New documentation will be created from scratch at the end
- Nuxt Content will be used for the new documentation site

### Design priorities

- Correctness over feature count
- Native type compatibility over fluent novelty
- Simple semantics over broad but inconsistent convenience APIs
- Clear migration breaks over partial backward compatibility

### Pendulum comparison policy

- Pendulum is the closest practical benchmark for Carbonic 2.0
- Pendulum is not a compatibility target by itself
- 2.0 should match or exceed Pendulum first on correctness-critical behavior:
  - exact instant preservation
  - timezone normalization
  - DST transition handling
  - native `datetime` interoperability
- Feature breadth only matters after semantics are defensible
- If Pendulum behavior conflicts with native stdlib semantics and no correctness bug is involved, native stdlib semantics win

## 2. Non-Goals for the First 2.0 Pass

- Reworking current MkDocs pages
- Preserving Carbon-style token compatibility
- Preserving every 1.x convenience API
- Expanding localization before core temporal semantics are correct
- Adding integrations before core types are stable

## 3. What Is Already Confirmed

- [x] `Date` as a wrapper does not type-check as `datetime.date`
- [x] A subclass of `datetime.date` does type-check as `datetime.date`
- [x] `DateTime` should follow the same subtype approach
- [x] 2.0 should drop Carbon-style date formatting tokens
- [x] Current docs should be ignored until the rewrite stabilizes

## 4. Main Problems to Fix from 1.x

### Core type design

- [x] Replace wrapper-style `Date` with a `datetime.date` subtype
- [ ] Replace wrapper-style `DateTime` with a `datetime.datetime` subtype
- [ ] Re-evaluate whether `Duration` should stay custom or become thinner over `datetime.timedelta`

### Parsing and formatting

- [ ] Remove Carbon token formatter/parser paths
- [ ] Define the supported Pythonic formatting subset
- [ ] Make platform-dependent behavior explicit in tests
- [ ] Prefer ISO parsing by default
- [ ] Require explicit formats for non-ISO parsing

### Timezone correctness

- [x] Preserve exact instants when parsing offset-aware datetimes
- [x] Stop silently coercing unknown timezones to UTC
- [x] Define how fixed offsets are represented internally
- [x] Ensure `from_datetime()` works on Windows and with local system zones

### API simplification

- [ ] Audit which 1.x helpers should survive unchanged
- [ ] Remove misleading or redundant convenience methods
- [ ] Decide whether business-day helpers belong in core 2.0
- [ ] Decide whether `Period` stays in 2.0
- [ ] Decide whether `Interval` ships in 2.0 initial release or a later phase

### Testing

- [ ] Add typing tests for native subtype compatibility
- [ ] Add cross-platform tests for formatting behavior
- [ ] Add strict timezone correctness tests
- [ ] Separate API tests from documentation tests
- [ ] Remove dependency on current docs for core validation

## 5. Implementation Phases

## Phase 0: Architecture Lock

Status: in progress

- [x] Confirm `Date` must be a `datetime.date` subtype
- [x] Confirm `DateTime` must be a `datetime.datetime` subtype
- [x] Write the exact 2.0 public API surface before coding
- [ ] Decide which 1.x modules are dropped, rewritten, or deferred

Exit criteria:
- one clear design for each public type
- no unresolved disagreement on type inheritance
- no remaining expectation of Carbon token support

## Phase 1: Date

Status: in progress

- [x] Implement `Date(datetime.date)`
- [x] Implement constructors/factories that still make sense
- [x] Preserve native date behavior
- [ ] Add Carbonic-specific helpers only where they remain justified
- [x] Ensure assignment to `datetime.date` is clean under static typing
- [x] Ensure comparisons with native `datetime.date` are natural

Exit criteria:
- `Date` behaves like a real date first
- `Date` passes runtime compatibility tests
- `Date` passes typing checks

## Phase 2: DateTime

Status: in progress

- [x] Implement `DateTime(datetime.datetime)`
- [x] Define timezone-aware versus naive behavior explicitly
- [x] Implement strict ISO parsing
- [x] Implement safe conversions from native datetimes
- [ ] Ensure assignment to `datetime.datetime` is clean under static typing

Exit criteria:
- `DateTime` preserves instants correctly
- `DateTime` is compatible with native datetime APIs
- `DateTime` passes typing and timezone tests

## Phase 3: Duration

Status: not started

- [ ] Decide whether `Duration` remains a custom type
- [ ] If custom, define exact semantics for calendar units versus exact time units
- [ ] Remove ambiguous comparison/arithmetic behavior
- [ ] Keep the API small and defensible

Exit criteria:
- duration semantics are explicit
- month/year behavior is not mixed carelessly with exact elapsed time

## Phase 4: Secondary Types

Status: not started

- [ ] Reassess `Interval`
- [ ] Reassess `Period`
- [ ] Reassess business-day helpers
- [ ] Move non-core features out of the critical path if needed

Exit criteria:
- only features with clear semantics remain in core 2.0

## Phase 5: Packaging and Test Cleanup

Status: not started

- [ ] Remove old docs-driven validation from the critical path
- [ ] Simplify dev dependencies where possible
- [ ] Align version metadata in package files
- [ ] Finalize CI around code and tests, not the old docs site

Exit criteria:
- repository validates the new codebase cleanly
- docs tooling is no longer a blocker for core development

## Phase 6: New Documentation

Status: deferred until core API stabilizes

- [ ] Scaffold Nuxt Content docs app
- [ ] Write 2.0 conceptual documentation from scratch
- [ ] Write API reference from actual 2.0 behavior
- [ ] Add migration guide from 1.x to 2.0

Exit criteria:
- docs match the rewritten API
- docs are built from the final design, not guessed in advance

## 6. Immediate Next Tasks

These are the next implementation tasks in order.

- [x] Define the exact public API for `Date(datetime.date)`
- [x] Define the exact public API for `DateTime(datetime.datetime)`
- [x] Finish the `DateTime(datetime.datetime)` subtype rewrite
- [x] Fix offset-aware parsing so parsed instants are preserved exactly
- [ ] Define DST-safe arithmetic and normalization rules with explicit transition tests
- [x] Remove `Date.format()` compatibility alias and keep `strftime()` / native `__format__` only
- [x] Make `Interval.duration()` return one consistent documented type
- [ ] Remove old guide docs from the critical validation path until the 2.0 API is frozen
- [ ] Decide the minimum viable 2.0 module list
- [ ] Decide which 1.x behaviors are intentionally breaking changes
- [x] Start implementation with `Date`

## 6A. Exact Public API: Date

This is the target public surface for the first 2.0 implementation pass.

### Construction and native behavior

- `class Date(datetime.date)`
- Construction stays native:

```python
Date(2026, 4, 24)
```

- Native behavior should be preserved by inheritance wherever possible:
  - `isoformat()`
  - `strftime()`
  - `weekday()`
  - `isoweekday()`
  - `isocalendar()`
  - `timetuple()`
  - `toordinal()`
  - `replace()`
  - built-in `format(date_obj, "%Y-%m-%d")`

### Class methods to keep

- `today(tz: str | datetime.tzinfo | None = None) -> Date`
  - if `tz is None`, use local system date
  - if `tz` is provided, use the current date in that timezone
- `tomorrow(tz: str | datetime.tzinfo | None = None) -> Date`
- `yesterday(tz: str | datetime.tzinfo | None = None) -> Date`
- `next(unit: Literal["day", "week", "month", "quarter", "year"], count: int = 1, tz: str | datetime.tzinfo | None = None) -> Date`
- `previous(unit: Literal["day", "week", "month", "quarter", "year"], count: int = 1, tz: str | datetime.tzinfo | None = None) -> Date`
- `from_date(value: datetime.date) -> Date`
- `parse(text: str, format_string: str | None = None) -> Date`
  - if `format_string is None`, parse ISO only
  - if `format_string` is provided, it must be Python `strptime` format only
  - Carbon tokens are not supported

### Instance methods to keep

- `add(*, years: int = 0, months: int = 0, weeks: int = 0, days: int = 0) -> Date`
- `subtract(*, years: int = 0, months: int = 0, weeks: int = 0, days: int = 0) -> Date`
- `next(weekday: Weekday, count: int = 1) -> Date`
- `previous(weekday: Weekday, count: int = 1) -> Date`
- `diff(other: datetime.date, *, absolute: bool = False) -> Duration`
- `start_of(unit: Literal["day", "week", "month", "quarter", "year"]) -> Date`
- `end_of(unit: Literal["day", "week", "month", "quarter", "year"]) -> Date`
- `is_weekday() -> bool`
- `is_weekend() -> bool`
- `add_business_days(days: int) -> Date`
- `subtract_business_days(days: int) -> Date`
- `to_datetime(tz: str | datetime.tzinfo | None = "UTC") -> datetime.datetime`
- `to_date() -> datetime.date`
  - returns a plain native `datetime.date`
  - kept mainly as a migration helper

### Formatting policy

- `strftime()` is the primary formatting API
- built-in `__format__` behavior from `datetime.date` is preferred
- `.format(...)` as a Carbon-style formatter does not survive 2.0
- there is no `.format(...)` compatibility alias on `Date`

### Explicit removals

- locale-aware token formatting on `Date`
- Carbon token parsing on `Date`
- ambiguous auto-parse of slash and dot formats

### Operator policy

- native operator behavior should be preserved where practical
- `Date - Date` should trend toward native `datetime.timedelta` semantics
- Carbonic-specific difference helpers belong on named methods such as `diff()`
- custom `Duration` operator integration is not part of the first `Date` rewrite pass
- `next` and `previous` intentionally support both:
  - class-level relative navigation from today
  - instance-level weekday navigation via `Weekday`

## 6B. Exact Public API: DateTime

This is the target public surface for the first 2.0 implementation pass.

### Construction and native behavior

- `class DateTime(datetime.datetime)`
- Construction should remain close to native `datetime.datetime`
- Support native `tzinfo=...`
- Also support Carbonic convenience `tz="Europe/Warsaw"` as an alias
- Preserve native behavior wherever possible:
  - `isoformat()`
  - `strftime()`
  - `astimezone()`
  - `date()`
  - `time()`
  - `timetz()`
  - `replace()`
  - `timestamp()`
  - `utcoffset()`
  - `dst()`
  - `tzname()`

### Native-semantics class methods

These must not keep misleading 1.x semantics.

- `now(tz: str | datetime.tzinfo | None = None) -> DateTime`
  - native semantics first
  - `None` means local naive current datetime
  - timezone string support is allowed as an extension
- `today() -> DateTime`
  - native semantics, not "today at midnight"

### Carbonic class methods to keep

- `from_datetime(value: datetime.datetime) -> DateTime`
- `parse(text: str, format_string: str | None = None, tz: str | datetime.tzinfo | None = None) -> DateTime`
  - if `format_string is None`, parse ISO only
  - if `format_string` is provided, it must be Python `strptime` format only
  - if parsed value is naive and `tz` is provided, attach that timezone
  - if parsed value is aware and `tz` is provided, convert to that timezone
  - Carbon tokens are not supported
- `tomorrow(tz: str | datetime.tzinfo | None = None) -> DateTime`
- `yesterday(tz: str | datetime.tzinfo | None = None) -> DateTime`
  - these are explicit convenience helpers
  - they should not change the semantics of native `today()`

### Instance methods to keep

- `add(*, years: int = 0, months: int = 0, weeks: int = 0, days: int = 0, hours: int = 0, minutes: int = 0, seconds: int = 0, microseconds: int = 0) -> DateTime`
- `subtract(...) -> DateTime`
- `diff(other: datetime.datetime, *, absolute: bool = False) -> Duration`
- `start_of(unit: Literal["minute", "hour", "day", "week", "month", "quarter", "year"]) -> DateTime`
- `end_of(unit: Literal["minute", "hour", "day", "week", "month", "quarter", "year"]) -> DateTime`
- `as_timezone(tz: str | datetime.tzinfo | None) -> DateTime`
- `to_date() -> Date`
- `to_datetime() -> datetime.datetime`
  - returns a plain native `datetime.datetime`
  - kept mainly as a migration helper

### Formatting policy

- `strftime()` is the primary formatting API
- built-in `datetime.__format__` behavior is preferred
- `.format(...)` as a Carbon-style formatter does not survive 2.0
- no `.format(...)` compatibility alias is planned for 2.0

### Explicit removals

- Carbon token formatting
- Carbon token parsing
- shortcut string methods whose behavior is already covered by native API:
  - `to_iso_string()`
  - `to_date_string()`
  - `to_time_string()`
  - `to_datetime_string()`
  - similar format-wrapper helpers unless they add real value

## 6C. Native Semantics Rules

These rules apply across the rewrite.

- If a Carbonic method has the same name as a native `date` or `datetime` method, native semantics win
- Convenience helpers may exist, but they must not redefine established stdlib names
- A helper that only duplicates native behavior without improving correctness should be removed
- Compatibility shims are acceptable only if they do not reintroduce 1.x ambiguity

## 6D. Pendulum Parity Checklist

Pendulum is the best external comparison point for Carbonic 2.0 because it already covers most of the hard datetime problems users expect a serious library to solve.

The parity goal is not "copy Pendulum".

The parity goal is:
- match Pendulum on correctness
- keep Carbonic features that are already better justified
- defer feature breadth that weakens native semantics

### Current strengths worth preserving

- [x] Keep business-day helpers if they remain small and correct
- [x] Keep interval set operations such as `contains()`, `overlaps()`, `intersection()`, and `union()` if `Interval` survives
- [x] Keep `Duration` semantics that separate calendar units from exact elapsed seconds instead of approximating everything into `timedelta`-style totals
- [x] Keep stdlib `zoneinfo` as the default timezone foundation
- [x] Keep first-party Pydantic integration if it does not distort the core API

### Release-gate parity with Pendulum

- [x] `DateTime` must be a real subtype of `datetime.datetime`, not a wrapper
- [x] Parsing offset-aware inputs must preserve the represented instant
  - `2025-09-23T14:30:45+02:00` must not silently become `2025-09-23T14:30:45+00:00`
- [x] Fixed-offset inputs must have a documented internal representation
- [x] `from_datetime()` must preserve meaningful `tzinfo` information for:
  - `zoneinfo.ZoneInfo`
  - fixed offsets
  - local system zones where possible
- [ ] DST transition arithmetic must be explicitly defined and tested for:
  - non-existing local times during spring-forward
  - ambiguous local times during fall-back
  - conversions that must preserve exact instants
- [ ] Formatting and parsing policy must be internally consistent across `Date` and `DateTime`
  - if Carbon tokens are removed, docs and tests must stop expecting them
  - do not reintroduce a `.format(...)` compatibility alias
- [x] `Interval.duration()` must return one documented type consistently, including `Date` intervals
- [ ] Core tests must no longer depend on old guide documentation matching 1.x behavior

### Near-term parity after core stability

- [ ] Support a strict ISO/RFC3339 parsing surface comparable to Pendulum's common inputs
- [ ] Reassess whether `Interval` should gain iteration/range behavior if it remains in core
- [ ] Reassess `next()`/`previous()` semantics on `DateTime` so they are explicit and native-friendly
- [ ] Reassess whether localized human-diff APIs beyond `Duration.humanize()` belong in core
- [ ] Decide whether test-time travel helpers belong in core, an optional extra, or nowhere in 2.0

### Deliberate non-parity

- [ ] No Carbon token compatibility in 2.0
- [ ] No lenient fallback parser comparable to Pendulum `strict=False` during the first pass
- [ ] No global mutable locale defaults until temporal semantics are stable
- [ ] No broad convenience surface that reuses stdlib names with changed meaning

## 7. Breaking Changes Expected in 2.0

- [ ] `Date` changes from wrapper object to native date subtype
- [x] `DateTime` changes from wrapper object to native datetime subtype
- [ ] Carbon token formatting is removed
- [ ] Lenient and ambiguous parsing is reduced or removed
- [ ] Some convenience methods may be dropped if they do not fit the new model
- [ ] Old docs examples will not be treated as compatibility targets

## 8. Notes

- 2.0 should be treated as a deliberate rewrite, not a compatibility patch release
- If a feature conflicts with native `datetime` semantics, native semantics win
- If typing and runtime behavior disagree, the API design is not finished yet

## 9. Validation Notes

- [x] `Date` now type-checks when assigned to `datetime.date`
- [x] basic native-subtype runtime checks passed
- [x] targeted relative-date tests still pass after the first `Date` rewrite
- [x] explicit `Date.parse(..., format_string=...)` now rejects incomplete formats such as `%Y-%m`
- [x] `Date(2026, 4, 1).next(Weekday.SUNDAY)` now resolves to `2026-04-05`
- [x] class-level `Date.next("week")` and `Date.previous("month")` still work
- [x] `tests/test_date.py` now passes against the 2.0 `Date` contract
- [x] `DateTime` now type-checks at runtime as a `datetime.datetime` subtype
- [x] `tests/test_datetime_v2.py` passes against the first 2.0 `DateTime` contract
- [x] offset-aware `DateTime.parse("2025-09-23T14:30:45+02:00")` preserves the represented instant
- [x] `Interval.duration()` now consistently returns `Duration`
- [ ] full 1.x test suite is intentionally not a compatibility target during the rewrite

## 9A. Current Snapshot Against Pendulum (2026-05-11)

- `.venv\Scripts\python.exe -m pytest` currently reports:
  - `377 passed`
  - `54 failed`
  - `2 skipped`
- The current failures are concentrated in:
  - old `DateTime` tests that still expect default UTC, midnight-style `today()`, Carbon `.format()`, and shortcut string helpers
  - locale and performance tests that still assume Carbon-style `.format(...)`
  - guide documentation that still reflects 1.x behavior
- Additional runtime gaps confirmed manually against current code:
  - DST arithmetic is not yet normalized correctly around spring-forward transitions
  - old documentation tests are still in the critical validation path
- Current areas where Carbonic is already stronger than Pendulum conceptually:
  - business-day helpers on `Date`
  - set-style interval operations
  - cleaner separation between calendar units and exact elapsed duration
  - first-party Pydantic integration
