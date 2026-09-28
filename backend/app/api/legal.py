from fastapi import APIRouter, Depends
from pydantic import BaseModel
from app.core.security import get_current_user
from app.models.user import User


router = APIRouter(
    prefix="/legal",
    tags=["AI Legal Assistant"]
)


class LegalQuestion(BaseModel):
    question: str


@router.post("/ask")
def ask_legal_question(
    data: LegalQuestion,
    current_user: User = Depends(get_current_user)
):
    question = data.question.lower()

    if any(word in question for word in [
        "cyber",
        "online fraud",
        "online scam",
        "fake account",
        "hacking",
        "phishing",
        "upi fraud"
    ]):
        answer = (
            "This appears to be related to cyber crime. "
            "Keep relevant evidence such as messages, screenshots and "
            "transaction details. Report the incident to the appropriate "
            "cyber crime authority and contact your bank or service provider "
            "if financial information is involved."
        )

    elif any(word in question for word in [
        "harassment",
        "stalking",
        "women safety",
        "sexual harassment",
        "domestic violence"
    ]):
        answer = (
            "This may involve a women's safety or harassment issue. "
            "If there is immediate danger, contact emergency services or "
            "the police. Preserve relevant evidence and consider seeking "
            "support from a trusted adult, authority or legal professional."
        )

    elif any(word in question for word in [
        "student",
        "college",
        "school",
        "exam",
        "marks",
        "scholarship"
    ]):
        answer = (
            "This appears to be an education-related grievance. "
            "First approach the appropriate faculty or institution grievance "
            "authority. Keep copies of applications, notices and other "
            "relevant documents."
        )

    elif any(word in question for word in [
        "lawyer",
        "court",
        "legal notice",
        "legal help",
        "legal advice"
    ]):
        answer = (
            "For a legal dispute, collect the relevant documents and "
            "consider consulting a qualified legal professional or an "
            "appropriate legal-aid service for advice specific to your case."
        )

    else:
        answer = (
            "I can provide general legal information, but this is not a "
            "substitute for advice from a qualified legal professional. "
            "Please describe the issue clearly, including the type of "
            "problem and the relevant circumstances."
        )

    return {
        "question": data.question,
        "answer": answer,
        "disclaimer": (
            "SafeConnect provides general information and does not replace "
            "professional legal advice."
        )
    }