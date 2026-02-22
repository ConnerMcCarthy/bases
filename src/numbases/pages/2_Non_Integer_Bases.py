"""Second Streamlit page for non-integer bases (starting with base-phi)."""
from __future__ import annotations

import math

import streamlit as st

from numbases.bases import PHI, from_non_integer_base, to_non_integer_base


st.set_page_config(page_title="Non-Integer Bases", page_icon="φ", layout="wide")

st.title("Non-Integer Bases")
st.caption("Experimental support using greedy digit expansion with finite precision.")

base_mode = st.radio(
    "Base mode",
    options=["Base phi (φ)", "Custom non-integer base"],
    horizontal=True,
)

if base_mode == "Base phi (φ)":
    base = PHI
    st.markdown(f"Using **φ = {PHI:.12f}**")
else:
    base = st.number_input(
        "Base (> 1, non-integer recommended)",
        min_value=1.000001,
        max_value=36.0,
        value=2.5,
        step=0.1,
        format="%.6f",
    )
    if abs(base - round(base)) < 1e-12:
        st.warning("This page is intended for non-integer bases; use the main page for integer bases.")

value_text = st.text_input("Decimal value to convert", value="10")
precision = st.slider("Fractional precision (digits after radix point)", min_value=0, max_value=30, value=18)

if st.button("Convert", type="primary"):
    try:
        value = float(value_text)
        if not math.isfinite(value):
            raise ValueError("value must be finite")

        encoded = to_non_integer_base(value, base, precision=precision)
        decoded = from_non_integer_base(encoded, base)
        error = abs(decoded - value)

        st.success("Converted successfully.")
        st.code(encoded, language="text")
        c1, c2, c3 = st.columns(3)
        c1.metric("Base", f"{base:.12g}")
        c2.metric("Round-trip decimal", f"{decoded:.12g}")
        c3.metric("Absolute error", f"{error:.3e}")
    except Exception as exc:
        st.error(f"Conversion error: {exc}")

st.markdown(
    """
    **Notes**
    - Digits are currently `0..floor(base)` using greedy selection.
    - Results are approximate for irrational bases like φ and finite precision.
    - A future update can add canonical normal forms for base-phi.
    """
)
