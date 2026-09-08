import os
from crewai import Agent, LLM

base_url = os.getenv("CREW_BASE_URL")

if base_url:
    # Local development Ollama
    llm = LLM(
        model=os.getenv("CREW_MODEL", "ollama/llama3.2:3b"),
        base_url=base_url,
    )
else:
    llm = LLM(
        model=os.getenv("CREW_MODEL", "llama-3.1-8b-instant"),
        base_url="https://api.groq.com/openai/v1",
        api_key=os.getenv("CREW_API_KEY"),
        custom_openai=True,
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