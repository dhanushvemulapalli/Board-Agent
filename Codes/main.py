import getpass
import os

from langgraph.graph import StateGraph, END
from langgraph.prebuilt import ToolNode
from typing import TypedDict, List
from langchain_core.messages import AIMessage, HumanMessage
from langchain_google_genai import ChatGoogleGenerativeAI

if "GOOGLE_API_KEY" not in os.environ:
    os.environ["GOOGLE_API_KEY"] = getpass.getpass("Enter your Google AI API key: ")

llm = ChatGoogleGenerativeAI(
        model="gemini-2.0-flash-thinking-exp-01-21",
        temperature=0.2
    )

from langgraph.channels import LastValue
from typing import TypedDict

# ✅ Correct usage
class ReviewState(TypedDict):
    proposal: LastValue[str]   # proposal is "last value" channel of type str
    legal_feedback: str
    ethics_feedback: str
    technical_feedback: str
    financial_feedback: str
    policy_feedback: str
    final_verdict: str

# Define agents with concise, structured prompts
def legal_advisor(state: ReviewState) -> ReviewState:
    print("Inside legal_advisor ")
    msg = f"""
You are a Legal Advisor.
Proposal: {state['proposal']}
Task: Identify legal risks under Indian Penal Code (IPC) and suggest modifications if needed.
Respond clearly with:
- Issues
- Suggested Fixes
- Verdict (Legal/Not Legal)
"""
    response = llm.invoke(msg).content
    state["legal_feedback"] = response
    return state


def ethics_expert(state: ReviewState) -> ReviewState:
    print("Inside ethics_expert ")

    msg = f"""
You are an Ethics Expert.
Proposal: {state['proposal']}
Task: Highlight ethical concerns and fairness issues.
Respond with:
- Key Ethical Risks
- Mitigation Suggestions
- Verdict (Ethical/Not Ethical)
"""
    response = llm.invoke(msg).content
    state["ethics_feedback"] = response
    return state


def financial_analyst(state: ReviewState) -> ReviewState:
    print("Inside financial_analyst ")

    msg = f"""
You are a Financial Analyst.
Proposal: {state['proposal']}
Task: Assess costs, ROI, and sustainability.
Respond with:
- Estimated Costs
- ROI & Risks
- Verdict (Financially Viable/Not Viable)
"""
    response = llm.invoke(msg).content
    state["financial_feedback"] = response
    return state


def technical_analyst(state: ReviewState) -> ReviewState:
    print("Inside technical_analyst ")

    msg = f"""
You are a Technical Analyst.
Proposal: {state['proposal']}
Task: Evaluate feasibility, technical risks, and limitations.
Respond with:
- Feasibility Issues
- Known Limitations
- Verdict (Feasible/Not Feasible)
"""
    response = llm.invoke(msg).content
    state["technical_feedback"] = response
    return state


def final_verdict(state: ReviewState) -> ReviewState:
    print("Inside final_verdict ")

    summary_prompt = f"""
Board Review Summary:

Legal: {state['legal_feedback']}
Ethics: {state['ethics_feedback']}
Financial: {state['financial_feedback']}
Technical: {state['technical_feedback']}

Task: Provide a final verdict.
Answer with:
- Overall Risk Level (Low/Medium/High)
- Deployment Recommendation (Yes/No)
- Short Rationale
"""
    response = llm.invoke(summary_prompt).content
    state["final_verdict"] = response
    return state

# Build LangGraph
builder = StateGraph(ReviewState)

builder.add_node("legal_advisor", legal_advisor)
builder.add_node("ethics_expert", ethics_expert)
builder.add_node("financial_analyst", financial_analyst)
builder.add_node("technical_analyst", technical_analyst)
builder.add_node("final_verdict", final_verdict)
builder.add_node("technical_analyst2", technical_analyst)




builder.set_entry_point("technical_analyst")

# Parallel paths

builder.add_edge("technical_analyst", "ethics_expert")
builder.add_edge("ethics_expert", "legal_advisor")
builder.add_edge("legal_advisor", "financial_analyst")
builder.add_edge("financial_analyst", "technical_analyst2")
builder.add_edge("technical_analyst2", "final_verdict")
builder.add_edge("final_verdict", END)

# Compile
graph = builder.compile()

# Run!
if __name__ == "__main__":
    user_input ="""
    We want to deploy an AI system in public schools that uses students' webcam footage during online exams to
    detect facial expressions and predict cheating behavior. The system flags suspicious behavior for review
    by school authorities.
    """

    initial_state = {
        "proposal": user_input,
        "legal_feedback": "",
        "ethics_feedback": "",
        "financial_feedback": "",
        "technical_feedback": "",
        "final_verdict": ""
    }
    result = graph.invoke(initial_state)

    print("\n🧾 Final Verdict:\n", result["final_verdict"])
    print("\n🧾 Legal Feedback:\n", result["legal_feedback"])
    print("\n🧾 Ethics Feedback:\n", result["ethics_feedback"])
    print("\n🧾 Financial Feedback:\n", result["financial_feedback"])
    print("\n🧾 Technical Feedback:\n", result["technical_feedback"])