import os
from crewai import Agent, LLM

base_url = os.getenv("CREW_BASE_URL")

if base_url:
    # Local development Ollama
    llm = LLM(
        model=os.getenv("CREW_MODEL", "openai/gpt-oss-20b"),
        base_url=base_url,
    )
else:
    # Production
    llm = LLM(
        model=os.getenv("CREW_MODEL", "llama-3.1-8b-instant"),
        base_url="https://api.groq.com/openai/v1",
        api_key=os.getenv("CREW_API_KEY"),
        custom_openai=True,
    )

credit_analyst = Agent(
    role="Credit Analyst",
    goal="Calculate the applicant's key financial ratios and summarize their affordability",
    backstory=(
        "You are a credit analyst at a lending institution. You review loan applications "
        "and compute standard financial ratios such as debt-to-income and loan-to-income "
        "to assess whether an applicant can reasonably afford the loan."
    ),
    llm=llm,
    verbose=True
)

risk_analyst = Agent(
    role="Risk Analyst",
    goal="Identify the specific factors that make this loan application risky or low risk",
    backstory=(
        "You are a risk analyst who reviews the credit analyst's findings along with the "
        "model's predicted default probability. You identify concrete risk factors and "
        "positive factors in the application, without repeating the credit analyst's ratios."
    ),
    llm=llm,
    verbose=True
)

underwriting_analyst = Agent(
    role="Underwriting Analyst",
    goal="Combine the credit and risk analysis into a final underwriting recommendation",
    backstory=(
        "You are a senior underwriter. You take the credit analyst's ratios and the risk "
        "analyst's findings and produce a final recommendation of Approve, Review, or "
        "Decline, along with a short list of reasons."
    ),
    llm=llm,
    verbose=True
)