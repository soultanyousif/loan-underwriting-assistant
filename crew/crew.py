import os
import joblib
from crewai import Crew, Process

from crew.agents import credit_analyst, risk_analyst, underwriting_analyst
from crew.tasks import credit_task, risk_task, underwriting_task
from model.features import build_features

MODEL_PATH = os.getenv("RISK_MODEL_PATH", "model/risk_model.joblib")
risk_model = joblib.load(MODEL_PATH)


def get_risk_band(probability):
    if probability < 0.10:
        return "LOW"
    elif probability < 0.25:
        return "MEDIUM"
    else:
        return "HIGH"


def build_application_summary(application):
    return (
        f"Annual income: {application['person_income']}\n"
        f"Employment length: {application['person_emp_length']} years\n"
        f"Home ownership: {application['person_home_ownership']}\n"
        f"Loan amount requested: {application['loan_amnt']}\n"
        f"Loan purpose: {application['loan_intent']}\n"
        f"Previous default on file: {application['cb_person_default_on_file']}\n"
        f"Credit history length: {application['cb_person_cred_hist_length']} years\n"
        f"Age: {application['person_age']}"
    )


def build_model_summary(probability, band):
    return (
        f"Predicted default probability: {round(probability * 100, 1)} percent\n"
        f"Risk band: {band}"
    )


def run_underwriting(application: dict) -> str:
    features = build_features(application)
    probability = risk_model.predict_proba(features)[0][1]
    band = get_risk_band(probability)

    crew = Crew(
        agents=[credit_analyst, risk_analyst, underwriting_analyst],
        tasks=[credit_task, risk_task, underwriting_task],
        process=Process.sequential,
        verbose=True
    )

    result = crew.kickoff(inputs={
        "application_summary": build_application_summary(application),
        "model_summary": build_model_summary(probability, band)
    })

    return str(result)



if __name__ == "__main__":
    test_application = {
        "person_age": 30,
        "person_income": 65000,
        "person_home_ownership": "RENT",
        "person_emp_length": 4,
        "loan_intent": "HOMEIMPROVEMENT",
        "loan_amnt": 25000,
        "cb_person_default_on_file": "N",
        "cb_person_cred_hist_length": 6
    }
    print(run_underwriting(test_application))