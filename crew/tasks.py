from crewai import Task
from crew.agents import credit_analyst, risk_analyst, underwriting_analyst

credit_task = Task(
    description=(
        "Applicant application data:\n"
        "{application_summary}\n\n"
        "Calculate and clearly state the following:\n"
        "- debt-to-income ratio\n"
        "- loan-to-income ratio\n"
        "- a short affordability assessment\n"
        "Keep the output factual and numeric, no recommendation yet."
    ),
    expected_output="A short summary with the calculated ratios and an affordability note.",
    agent=credit_analyst
)

risk_task = Task(
    description=(
        "Applicant application data:\n"
        "{application_summary}\n\n"
        "Model prediction:\n"
        "{model_summary}\n\n"
        "Based on the application and the model's predicted default probability, list:\n"
        "- positive factors that lower risk\n"
        "- risk factors that raise concern\n"
        "Do not repeat the ratios from the credit analyst, focus on what they imply."
    ),
    expected_output="A short list of positive factors and risk factors.",
    agent=risk_analyst,
    context=[credit_task]
)

underwriting_task = Task(
    description=(
        "Applicant application data:\n"
        "{application_summary}\n\n"
        "Model prediction:\n"
        "{model_summary}\n\n"
        "Using the credit analyst's ratios and the risk analyst's factors, produce a final "
        "recommendation in this exact format:\n\n"
        "RECOMMENDATION: <Approve, Review, or Decline>\n"
        "RISK: <Low, Medium, or High>\n"
        "REASONS:\n"
        "- <reason 1>\n"
        "- <reason 2>\n"
        "- <reason 3>"
    ),
    expected_output="A final recommendation in the exact format described, nothing else.",
    agent=underwriting_analyst,
    context=[credit_task, risk_task]
)