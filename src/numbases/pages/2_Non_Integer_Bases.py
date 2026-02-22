"""Second Streamlit page for non-integer bases (starting with base-phi)."""
from __future__ import annotations

import math

import streamlit as st

from numbases.bases import (
    PHI,
    canonicalize_phi_digits,
    from_base_phi_exact,
    from_non_integer_base,
    is_canonical_phi_digits,
    phi_digits_to_expression,
    to_base_phi_exact,
    to_non_integer_base,
)


st.set_page_config(page_title="Non-Integer Bases", page_icon="🧮", layout="wide")

st.markdown(
    """
    <style>
    .stApp {
        color: #0f172a;
        background:
            radial-gradient(circle at 20% 10%, #dbeafe 0, transparent 40%),
            radial-gradient(circle at 80% 15%, #fde68a 0, transparent 35%),
            linear-gradient(160deg, #f8fafc 0%, #eef2ff 100%);
    }
    .stApp, .stApp p, .stApp label, .stApp h1, .stApp h2, .stApp h3 {
        color: #0f172a !important;
    }
    .stTextInput > div > div > input,
    .stNumberInput input {
        background: #ffffff !important;
        color: #0f172a !important;
        border: 1px solid #94a3b8 !important;
    }
    .stButton > button,
    button[data-testid="stBaseButton-secondary"],
    button[data-testid="stBaseButton-primary"] {
        background: #f8fafc !important;
        color: #0f172a !important;
        border: 1px solid #64748b !important;
    }
    .stButton > button:hover,
    button[data-testid="stBaseButton-secondary"]:hover,
    button[data-testid="stBaseButton-primary"]:hover {
        background: #e2e8f0 !important;
        color: #0f172a !important;
        border-color: #334155 !important;
    }
    .stButton > button:focus,
    button[data-testid="stBaseButton-secondary"]:focus,
    button[data-testid="stBaseButton-primary"]:focus {
        box-shadow: 0 0 0 2px #93c5fd !important;
        color: #0f172a !important;
    }
    div[data-testid="stMetric"] {
        background: rgba(255, 255, 255, 0.86);
        border: 1px solid #cbd5e1;
        border-radius: 10px;
        padding: 0.6rem 0.8rem;
    }
    div[data-testid="stMetricLabel"] p,
    div[data-testid="stMetricValue"] {
        color: #0f172a !important;
    }
    header[data-testid="stHeader"] {
        background: rgba(248, 250, 252, 0.9) !important;
        border-bottom: 1px solid #cbd5e1;
    }
    header[data-testid="stHeader"] * {
        color: #0f172a !important;
    }
    div[data-testid="stSidebarNav"] {
        background: rgba(255, 255, 255, 0.88);
        border-right: 1px solid #cbd5e1;
    }
    div[data-testid="stSidebarNav"] a,
    div[data-testid="stSidebarNav"] span {
        color: #0f172a !important;
    }
    div[data-testid="stSidebarNav"] a:hover {
        background: #e2e8f0;
    }
    .top-nav {
        display: flex;
        gap: .6rem;
        align-items: center;
        margin: .2rem 0 1rem 0;
        padding: .4rem .5rem;
        border: 1px solid #cbd5e1;
        border-radius: 10px;
        background: rgba(255,255,255,.82);
    }
    </style>
    """,
    unsafe_allow_html=True,
)

st.markdown('<div class="top-nav"></div>', unsafe_allow_html=True)
n1, n2, _ = st.columns([1, 1, 6])
with n1:
    st.page_link("web_ui.py", label="Base Explorer", icon="🔢")
with n2:
    st.page_link("pages/2_Non_Integer_Bases.py", label="Base φ", icon="🧮")

st.title("Non-Integer Bases")
st.caption("Experimental support using greedy digit expansion with finite precision.")

PLASTIC_CONSTANT = 1.3247179572447458

base_mode = st.radio(
    "Base mode",
    options=[
        "Base phi (φ)",
        "Base pi (π)",
        "Base pi/2 (π/2)",
        "Base plastic constant (ρ)",
        "Custom non-integer base",
    ],
    horizontal=True,
)

if base_mode == "Base phi (φ)":
    base = PHI
    st.markdown(f"Using **φ = {PHI:.12f}**")
elif base_mode == "Base pi (π)":
    base = math.pi
    st.markdown(f"Using **π = {math.pi:.12f}**")
elif base_mode == "Base pi/2 (π/2)":
    base = math.pi / 2
    st.markdown(f"Using **π/2 = {math.pi / 2:.12f}**")
elif base_mode == "Base plastic constant (ρ)":
    base = PLASTIC_CONSTANT
    st.markdown(f"Using **ρ = {PLASTIC_CONSTANT:.12f}**")
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
phi_engine = "Floating approximation"
if base_mode == "Base phi (φ)":
    phi_engine = st.radio(
        "Base-φ conversion mode",
        options=["Exact integer canonical", "Floating approximation"],
        horizontal=True,
        help="Exact mode requires an integer decimal input and enforces canonical no-adjacent-ones digits.",
    )

if st.button("Convert", type="primary"):
    try:
        if base_mode == "Base phi (φ)" and phi_engine == "Exact integer canonical":
            if "." in value_text.strip():
                raise ValueError("exact base-φ mode requires an integer input (no decimal point)")
            value_int = int(value_text.strip())
            encoded = to_base_phi_exact(value_int)
            decoded = from_base_phi_exact(encoded)
            error = 0.0

            st.success("Converted successfully (exact canonical mode).")
            st.code(encoded, language="text")
            c1, c2, c3 = st.columns(3)
            c1.metric("Base", "phi (exact)")
            c2.metric("Round-trip integer", str(decoded))
            c3.metric("Absolute error", f"{error:.1f}")
        else:
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

st.divider()
st.subheader("Base-φ Number Inspector")
st.caption("Enter base-φ digits and get symbolic φ terms plus decimal value.")

phi_digits_input = st.text_input(
    "Base-φ digits",
    value="101.01",
    help="Use only 0/1 with optional decimal point, e.g. 101, 1000.01, -10.1",
)

if st.button("Inspect base-φ number"):
    try:
        canonical = canonicalize_phi_digits(phi_digits_input)
        symbolic = phi_digits_to_expression(canonical)
        decimal_value = from_non_integer_base(canonical, PHI)
        canonical_flag = is_canonical_phi_digits(phi_digits_input)

        st.success("Parsed successfully.")
        c1, c2, c3 = st.columns(3)
        c1.markdown("**φ representation**")
        c1.code(symbolic, language="text")
        c2.markdown("**Decimal value**")
        c2.code(f"{decimal_value:.12g}", language="text")
        c3.markdown("**Canonical digits**")
        c3.code(canonical, language="text")
        if canonical_flag:
            st.caption("Input is already canonical (no adjacent ones).")
        else:
            st.caption("Input was normalized to canonical form (no adjacent ones).")
    except Exception as exc:
        st.error(f"Inspector error: {exc}")
