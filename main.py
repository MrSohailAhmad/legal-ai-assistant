import os
import streamlit as st
from dotenv import load_dotenv
from pypdf import PdfReader

load_dotenv()

from src.generate import analyze_contract

st.set_page_config(page_title="Legal AI Assistant", page_icon="⚖️")
st.title("⚖️ Legal AI Assistant")
st.caption("Upload a contract. Get structured clause analysis and risk flags.")

# Sidebar for API key configuration / overrides
api_key = os.getenv("OPENAI_API_KEY")
if not api_key:
    try:
        api_key = st.secrets.get("OPENAI_API_KEY")
    except Exception:
        pass

with st.sidebar:
    st.header("⚙️ Configuration")
    user_api_key = st.text_input(
        "OpenAI API Key",
        type="password",
        value=api_key or "",
        help="Provide your OpenAI API key here or add it to Streamlit Secrets / .env",
    )
    if user_api_key:
        api_key = user_api_key

uploaded = st.file_uploader("Upload contract (PDF)", type="pdf")

if uploaded and st.button("Analyze"):
    if not api_key:
        st.error(
            "⚠️ **OpenAI API Key is missing.**\n\n"
            "Please enter your key in the sidebar, or configure `OPENAI_API_KEY` in your "
            "`.env` file (locally) or in **Settings > Secrets** on Streamlit Cloud."
        )
        st.stop()

    with st.spinner("Reading contract..."):
        reader = PdfReader(uploaded)
        text = "\n".join(p.extract_text() or "" for p in reader.pages)

    if not text.strip():
        st.warning(
            "Could not extract any text from this PDF. Please check if the PDF contains scanned images instead of text."
        )
        st.stop()

    with st.spinner("Analyzing clauses with AI..."):
        try:
            result = analyze_contract(text, api_key=api_key)
        except Exception as e:
            st.error(f"Error during contract analysis: {e}")
            st.stop()

    st.subheader("Summary")
    st.write(f"**Parties:** {', '.join(result.parties)}")
    st.write(f"**Effective date:** {result.effective_date or 'Not found'}")
    st.write(f"**Overall risk:** {result.overall_risk.upper()}")

    if result.red_flags:
        st.subheader("🚩 Red Flags")
        for flag in result.red_flags:
            st.warning(flag)

    st.subheader("Clauses")
    for clause in result.clauses:
        color = {"low": "green", "medium": "orange", "high": "red"}[clause.risk_level]
        with st.expander(
            f"{clause.clause_type} — :{color}[{clause.risk_level.upper()}]"
        ):
            st.write(clause.summary)
            st.caption(clause.risk_reason)
