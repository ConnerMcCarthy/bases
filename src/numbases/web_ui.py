"""Streamlit web UI for exploring number base conversions."""
from __future__ import annotations

import streamlit as st

from numbases.bases import factors, from_base, to_base, to_base_parenthesized


def render() -> None:
    st.set_page_config(page_title="numbases web explorer", page_icon="🔢", layout="wide")
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
        .block-container { padding-top: 1.6rem; }
        .hero {
            background: rgba(255,255,255,0.7);
            border: 1px solid #bfdbfe;
            border-radius: 14px;
            padding: 1rem 1.2rem;
            margin-bottom: 1rem;
        }
        .stTextInput > div > div > input,
        .stNumberInput input {
            background: #ffffff !important;
            color: #0f172a !important;
            border: 1px solid #94a3b8 !important;
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
        .stCodeBlock {
            border: 1px solid #cbd5e1;
            border-radius: 10px;
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

    st.markdown(
        """
        <div class="hero">
          <h2 style="margin:0">Number Base Explorer</h2>
          <p style="margin:.4rem 0 0">Convert any integer representation between bases 2 and 36.</p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    left, right = st.columns([1.2, 1], gap="large")

    with left:
        st.subheader("Input")
        number_text = st.text_input("Number", value="101")
        input_base = st.number_input("Input base", min_value=2, max_value=36, value=2, step=1)
        custom_base = st.number_input("Custom output base", min_value=2, max_value=36, value=3, step=1)
        parenthesized_digits = st.checkbox(
            "Use parenthesized digits for values >= 10",
            value=False,
            help="Example: base-36 digits can appear like (34)(32) instead of YW.",
        )
        convert_clicked = st.button("Convert", type="primary")

    with right:
        st.subheader("How it works")
        st.write(
            "1. Parse your input using the selected base.\n"
            "2. Convert to decimal internally.\n"
            "3. Render outputs in common and custom bases."
        )

    if not convert_clicked:
        st.info("Adjust values and click Convert.")
        return

    try:
        decimal = from_base(number_text.strip(), int(input_base))
    except Exception as exc:
        st.error(f"Conversion error: {exc}")
        return

    st.success("Converted successfully.")
    st.metric("Decimal", value=str(decimal))

    formatter = to_base_parenthesized if parenthesized_digits else to_base

    common_bases = [2, 8, 10, 16, 36]
    st.subheader("Common Outputs")
    cols = st.columns(len(common_bases))
    for col, base in zip(cols, common_bases):
        col.metric(f"Base {base}", formatter(decimal, base))

    st.subheader("Custom Output")
    st.code(formatter(decimal, int(custom_base)), language="text")

    st.subheader("Factors")
    if decimal == 0:
        st.info("0 has infinitely many divisors, so factors are not listed.")
    else:
        factor_values = factors(decimal)
        st.write(f"Factors of |{decimal}| ({len(factor_values)} total):")
        st.code(", ".join(str(value) for value in factor_values), language="text")


def main() -> None:
    render()


if __name__ == "__main__":
    main()
