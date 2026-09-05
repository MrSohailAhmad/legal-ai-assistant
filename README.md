# ⚖️ Legal AI Assistant

An intelligent, AI-powered legal contract analysis application built with **Streamlit**, **Google GenAI (Gemini Structured Outputs with Pydantic)**, and **PyPDF**.

Upload any legal contract in PDF format to automatically extract contracting parties, key dates, assess overall risk, flag potential legal pitfalls, and receive structured clause-by-clause risk breakdowns with full reasoning.

---

## 🌟 Key Features

- **Automated PDF Ingestion**: Extracts text directly from multi-page contract PDFs using `pypdf`.
- **Guaranteed Structured Outputs**: Uses Google GenAI's native `response_schema` with **Pydantic v2** models (`ContractAnalysis` and `Clause`) to eliminate JSON parsing errors and hallucinated schemas.
- **Contract Metadata Extraction**: Identifies contracting parties and effective start dates accurately.
- **Clause-by-Clause Risk Evaluation**: Breaks down clauses (e.g., Termination, Liability, Confidentiality, Intellectual Property) with human-readable summaries, risk levels (`low`, `medium`, `high`), and explicit risk rationales.
- **Red Flag Detection**: Flags dangerous, ambiguous, or one-sided terms immediately with visual warning banners.
- **Interactive Streamlit UI**: Intuitive web dashboard featuring expandable clause cards color-coded by severity (🟢 Low, 🟠 Medium, 🔴 High).

---

## 🏗️ Architecture & Pipeline Flow

```
   [ Upload Contract PDF ]
              │
              ▼
   [ Text Extraction ]          ──> pypdf extracts text across all pages
              │
              ▼
   [ Google GenAI (Gemini) ]    ──> gemini-2.5-flash with structured output enforcement
              │                      (ContractAnalysis Pydantic schema)
              ▼
   [ Validated Schema Object ]  ──> Parties, Effective Date, Overall Risk,
              │                      Red Flags & Clause-level Risk Ratings
              ▼
   [ Streamlit Dashboard ]      ──> Visual summary cards, alert callouts for
                                      red flags, and color-coded expandable clauses
```

---

## 💻 Tech Stack

| Technology | Purpose | Description |
| :--- | :--- | :--- |
| **Python 3.12+** | Core Runtime | Modern Python with type annotations |
| **Streamlit** | Frontend UI | Web dashboard for file upload and interactive results presentation |
| **Google GenAI SDK** | LLM Engine | `gemini-2.5-flash` with native Pydantic structured output enforcement |
| **Pydantic v2** | Schema Validation | Type-safe contract schema definition (`ContractAnalysis`, `Clause`) |
| **PyPDF** | Document Parsing | Pure-Python library for reading and extracting text from PDF files |
| **python-dotenv** | Environment Config | Securely loads configuration and API keys from `.env` |
| **uv** | Package Management | Fast Python package and dependency resolver |

---

## 📁 Project Structure

```text
legal-ai-assistant/
├── main.py             # Streamlit application entrypoint & UI layout
├── pyproject.toml      # Project configuration & package dependencies
├── pyrightconfig.json  # Type checker configuration
├── uv.lock             # Exact dependency lockfile for reproducible builds
├── .python-version     # Python runtime specification (3.12)
├── .env.example        # Template for required environment variables
├── README.md           # Project documentation
└── src/
    ├── __init__.py     # Package marker
    ├── schema.py       # Pydantic schemas (ContractAnalysis, Clause)
    └── generate.py     # Google GenAI client & structured contract analysis logic
```

---

## 🚀 Getting Started & Setup

### 1. Prerequisites

- **Python 3.12** or higher
- A **Gemini API Key** ([Google AI Studio](https://aistudio.google.com/app/apikey))
- *(Recommended)* **[uv](https://github.com/astral-sh/uv)** installed on your machine

---

### 2. Clone the Repository

```bash
git clone <repository-url>
cd legal-ai-assistant
```

---

### 3. Configure Environment Variables

Copy the example environment file:

```bash
cp .env.example .env
```

Open `.env` in your text editor and add your Gemini API key:

```env
GEMINI_API_KEY=your_actual_gemini_api_key_here
```

---

### 4. Install Dependencies

You can install dependencies using **uv** (recommended) or standard **pip / venv**.

#### Option A: Using `uv` (Fastest)

```bash
uv sync
```

#### Option B: Using Standard `pip` and Virtualenv

```bash
# Create and activate virtual environment
python3 -m venv .venv
source .venv/bin/activate   # On Windows: .venv\Scripts\activate

# Install dependencies
pip install -e .
```

---

### 5. Run the Application

#### With `uv`:
```bash
uv run streamlit run main.py
```

#### With an active virtual environment:
```bash
streamlit run main.py
```

Open your browser and navigate to `http://localhost:8501`.

---

## 📖 How to Use

1. **Upload a Contract**: Click **"Upload contract (PDF)"** and select your legal agreement (e.g., NDA, Employment Agreement, SaaS Terms of Service, Vendor Contract).
2. **Configure Key**: Enter your Gemini API Key in the sidebar or keep it in `.env` / Streamlit Secrets.
3. **Run Analysis**: Click the **"Analyze"** button.
4. **Review Summary**: View identified contracting parties, effective date, and overall agreement risk.
5. **Inspect Red Flags**: Read any high-priority warnings or critical issues highlighted at the top.
6. **Explore Clauses**: Click through the expandable clause sections to see summaries, risk levels, and specific explanations for why each risk level was assigned.

---

## ⚙️ Customization

- **Change the Model**: In [`src/generate.py`](file:///Users/macbook/Documents/courses/zaphrix/rag/legal-ai-assistant/src/generate.py) or `.env`, configure `GEMINI_MODEL=gemini-2.5-pro` (defaults to `gemini-2.5-flash`).
- **Extend the Schema**: In [`src/schema.py`](file:///Users/macbook/Documents/courses/zaphrix/rag/legal-ai-assistant/src/schema.py), add new fields to `ContractAnalysis` (such as `governing_law: str | None`, `jurisdiction: str | None`, or `payment_terms: str | None`).

---

## 📄 License

MIT License. Feel free to use, modify, and distribute for your own projects.
