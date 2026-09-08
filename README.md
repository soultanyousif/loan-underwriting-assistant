# Loan Application Underwriting Assistant

A loan underwriting demo combining a calibrated XGBoost default-risk model with a
CrewAI multi-agent pipeline that explains the risk in plain language and produces
an Approve / Review / Decline recommendation.

**Live demo:** https://loan-underwriting-assistant.onrender.com/ui/

> Note: the app runs on Render's free tier, so it spins down after inactivity.
> The first request after idle time can take 30-60 seconds to wake up.

## How it works

1. The applicant submits standard loan application fields (income, employment,
   loan amount, purpose, etc) through a simple web form.
2. A calibrated XGBoost model predicts a default probability from those fields.
3. The probability is mapped to a risk band (LOW / MEDIUM / HIGH).
4. Three CrewAI agents (Credit Analyst, Risk Analyst, Underwriting Analyst) take
   the applicant data and the model's prediction and produce a final written
   recommendation, running on Groq's `openai/gpt-oss-20b` model.

## Data

Trained on the [Credit Risk Dataset](https://www.kaggle.com/datasets/laotse/credit-risk-dataset)
from Kaggle, which contains loan applicant records with fields such as income,
employment length, home ownership, loan purpose, loan amount, prior default status,
credit history length, and a binary loan-status label.

## Tech stack

- **Model:** XGBoost, calibrated with scikit-learn, trained in `notebook/model.ipynb`
- **Agents:** CrewAI, three sequential agents (Credit Analyst → Risk Analyst → Underwriting Analyst)
- **LLM:** Groq (`openai/gpt-oss-20b`) in production, Ollama locally for development
- **API:** FastAPI, served with Uvicorn
- **UI:** a single static HTML/JS page served at `/ui/`
- **Hosting:** Docker container on Render's free tier

## Try it

- Use the web form at `/ui/` for a friendly interface.
- Or POST directly to `/assess` with a JSON body matching the `LoanApplication`
  schema, or use the interactive API docs at `/docs`.

Example request body:

```json
{
  "person_age": 35,
  "person_income": 65000,
  "person_home_ownership": "MORTGAGE",
  "person_emp_length": 8,
  "loan_intent": "DEBTCONSOLIDATION",
  "loan_amnt": 15000,
  "cb_person_default_on_file": "N",
  "cb_person_cred_hist_length": 10
}
```

## Running locally

1. Install dependencies: `pip install -r requirements.txt`
2. Run Ollama locally with a small model, e.g. `ollama run llama3.2:3b`
3. Set `CREW_BASE_URL=http://localhost:11434` in a local `.env` file (see `.env.example` if present)
4. Start the app: `uvicorn app:app --reload`
5. Visit `http://localhost:8000/ui/`

## Limitations

This is a portfolio / demonstration project, not a production credit model.
Notably:

- No fair lending / disparate impact testing has been performed (the dataset
  has no protected-class fields to test against).
- Adverse action reasoning is LLM-generated and has not been legally reviewed.
- Trained on a public Kaggle dataset of unknown real-world representativeness,
  not a real lender's applicant population.
- The model appears to weight "no default on file" heavily, which may partly
  reflect thin credit history rather than genuinely low risk — worth further
  investigation before any real use.
