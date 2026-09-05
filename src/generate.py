from openai import OpenAI

# pyrefly: ignore [missing-import]
from src.schema import ContractAnalysis

client = OpenAI()


def analyze_contract(text: str) -> ContractAnalysis:

    resp = client.chat.completions.create(
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
    return resp.choices[0].message.parsed
