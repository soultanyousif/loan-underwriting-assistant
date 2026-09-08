---
title: Loan Underwriting Assistant
emoji: 📋
colorFrom: blue
colorTo: gray
sdk: docker
app_port: 7860
pinned: false
---

# Loan Application Underwriting Assistant

A loan underwriting demo combining a calibrated XGBoost default-risk model with a
CrewAI multi-agent pipeline that explains the risk in plain language and produces
an Approve / Review / Decline recommendation.

## How it works

1. The applicant submits standard loan application fields (income, employment,
   loan amount, purpose, etc).
2. A calibrated XGBoost model predicts a default probability from those fields.
3. The probability is mapped to a risk band (LOW / MEDIUM / HIGH).
4. Three CrewAI agents (Credit Analyst, Risk Analyst, Underwriting Analyst) take
   the applicant data and the model's prediction and produce a final written
   recommendation.

## Try it

POST to `/assess` with a JSON body matching the `LoanApplication` schema, or use
the interactive docs at `/docs`.

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