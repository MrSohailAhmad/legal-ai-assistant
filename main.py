import streamlit as st
from dotenv import load_dotenv
from pypdf import PdfReader

# pyrefly: ignore [missing-import]
from src.generate import analyze_contract

load_dotenv()
st.set_page_config(page_title="Legal AI Assistant", page_icon="⚖️")
st.title("⚖️ Legal AI Assistant")
st.caption("Upload a contract. Get structured clause analysis and risk flags.")

uploaded = st.file_uploader("Upload contract (PDF)", type="pdf")

if uploaded and st.button("Analyze"):
    with st.spinner("Reading contract..."):
        reader = PdfReader(uploaded)
        text = "\n".join(p.extract_text() or "" for p in reader.pages)

    with st.spinner("Analyzing clauses..."):
        result = analyze_contract(text)

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
