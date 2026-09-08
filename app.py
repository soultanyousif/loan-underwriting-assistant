from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from schemas import LoanApplication, UnderwritingResponse
from crew.crew import run_underwriting, build_features, risk_model, get_risk_band

app = FastAPI(title="Loan Underwriting Assistant")

app.mount("/ui", StaticFiles(directory="static", html=True), name="ui")


@app.get("/")
def root():
    return {"status": "ok"}


@app.post("/assess", response_model=UnderwritingResponse)
def assess(application: LoanApplication):
    application_dict = application.model_dump()

    features = build_features(application_dict)
    probability = float(risk_model.predict_proba(features)[0][1])
    band = get_risk_band(probability)

    assessment = run_underwriting(application_dict)

    return UnderwritingResponse(
        default_probability=round(probability, 4),
        risk_band=band,
        assessment=assessment
    )