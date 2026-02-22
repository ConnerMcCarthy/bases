# Base-Phi Design Notes

## Decision

Implement a design-first plan before coding `to_base_phi` and `from_base_phi`.

## Goal

Support representation of integers in base `phi` (the golden ratio),
with deterministic normalized output.

## Constraints

- Base is irrational, so standard repeated division/modulo does not apply.
- Multiple representations can exist unless canonical rules are enforced.
- We need reliable round-trip behavior for integer values.

## Proposed Representation

- Digits: `0` and `1`
- Positional powers of `phi`
- Canonical rule: no adjacent `1` digits in the normalized output
- Optional sign prefix `-` for negatives

Example shape (illustrative only):
- `100100.01_phi`

## Algorithm Outline

1. Compute a raw expansion from the target integer using greedy selection of
   powers of `phi`.
2. Normalize with rewrite rules to eliminate adjacent ones:
   - `11 -> 100` (applied with carry behavior across the radix point as needed)
3. Trim leading/trailing zeros.
4. Return canonical string.

For parsing:
1. Validate characters (`0`, `1`, optional `.` and leading `-`).
2. Evaluate weighted sum using powers of `phi`.
3. Snap to nearest integer with tolerance for floating error.
4. Reject non-integer outcomes unless explicit fractional mode is added.

## Milestones

1. Implement `to_base_phi(int) -> str` for non-negative integers.
2. Add normalization tests (no adjacent ones in output).
3. Add signed integer support.
4. Implement `from_base_phi(str) -> int` with strict validation.
5. Add round-trip property tests over a range (e.g. `-500..500`).

## Testing Strategy

- Known value fixtures for small integers.
- Property test: `from_base_phi(to_base_phi(n)) == n`.
- Canonicality test: output contains no adjacent `1`.
- Error-path tests for malformed strings.
