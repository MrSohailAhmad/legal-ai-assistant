import os
from google import genai
from google.genai import types
from .schema import ContractAnalysis


def get_genai_client(api_key: str | None = None) -> genai.Client:
    """Resolve and return a Google GenAI client with lazy initialization."""
    if api_key:
        return genai.Client(api_key=api_key)

    key = os.getenv("GEMINI_API_KEY") or os.getenv("GOOGLE_API_KEY")
    if not key:
        try:
            import streamlit as st
            key = st.secrets.get("GEMINI_API_KEY") or st.secrets.get("GOOGLE_API_KEY")
        except Exception:
            pass

    if not key:
        raise ValueError(
            "Gemini API key not found. Please set GEMINI_API_KEY (or GOOGLE_API_KEY) in your environment, "
            ".env file, or Streamlit Cloud Secrets."
        )

    return genai.Client(api_key=key)


def analyze_contract(
    text: str,
    api_key: str | None = None,
    model: str | None = None,
) -> ContractAnalysis:
    """Analyze contract text and extract structured clauses using Google GenAI."""
    client = get_genai_client(api_key)
    target_model = model or os.getenv("GEMINI_MODEL", "gemini-2.5-flash")

    config = types.GenerateContentConfig(
        system_instruction="You are a contract analysis assistant. Extract structured data only from what's in the document.",
        response_mime_type="application/json",
        response_schema=ContractAnalysis,
    )

    resp = client.models.generate_content(
        model=target_model,
        contents=f"Analyze this contract:\n\n{text}",
        config=config,
    )

    if resp.parsed is not None:
        if isinstance(resp.parsed, ContractAnalysis):
            return resp.parsed
        return ContractAnalysis.model_validate(resp.parsed)

    if resp.text:
        return ContractAnalysis.model_validate_json(resp.text)

    raise ValueError("Failed to obtain structured contract analysis from Gemini model response.")
