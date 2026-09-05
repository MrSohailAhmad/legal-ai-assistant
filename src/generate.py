import os
from openai import OpenAI
from .schema import ContractAnalysis


def get_openai_client(api_key: str | None = None) -> OpenAI:
    """Resolve and return an OpenAI client with lazy initialization."""
    if api_key:
        return OpenAI(api_key=api_key)

    key = os.getenv("OPENAI_API_KEY")
    if not key:
        try:
            import streamlit as st
            key = st.secrets.get("OPENAI_API_KEY")
        except Exception:
            pass

    if not key:
        raise ValueError(
            "OpenAI API key not found. Please set OPENAI_API_KEY in your environment, "
            ".env file, or Streamlit Cloud Secrets."
        )

    return OpenAI(api_key=key)


def analyze_contract(text: str, api_key: str | None = None) -> ContractAnalysis:
    client = get_openai_client(api_key)

    resp = client.beta.chat.completions.parse(
        model="gpt-4o-mini",
        messages=[
            {
                "role": "system",
                "content": "You are a contract analysis assistant. Extract structured data only from what's in the document.",
            },
            {"role": "user", "content": f"Analyze this contract:\n\n{text}"},
        ],
        response_format=ContractAnalysis,
    )
    parsed = resp.choices[0].message.parsed
    if parsed is None:
        raise ValueError("Failed to parse contract analysis from model response.")
    return parsed
