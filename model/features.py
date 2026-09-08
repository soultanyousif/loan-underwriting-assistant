import pandas as pd

CATEGORICAL_COLS = ["person_home_ownership", "loan_intent", "cb_person_default_on_file"]
NUMERIC_COLS = ["person_age", "person_income", "person_emp_length", "loan_amnt",
                 "loan_percent_income", "cb_person_cred_hist_length"]


def build_features(application: dict) -> pd.DataFrame:
    loan_percent_income = application["loan_amnt"] / application["person_income"]

    row = {
        "person_age": application["person_age"],
        "person_income": application["person_income"],
        "person_home_ownership": application["person_home_ownership"],
        "person_emp_length": application["person_emp_length"],
        "loan_intent": application["loan_intent"],
        "loan_amnt": application["loan_amnt"],
        "loan_percent_income": loan_percent_income,
        "cb_person_default_on_file": application["cb_person_default_on_file"],
        "cb_person_cred_hist_length": application["cb_person_cred_hist_length"],
    }

    return pd.DataFrame([row], columns=CATEGORICAL_COLS + NUMERIC_COLS)