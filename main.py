import getpass
import os

if "GOOGLE_API_KEY" not in os.environ:
    os.environ["GOOGLE_API_KEY"] = getpass.getpass("Enter your Google AI API key: ")

from langgraph.graph import StateGraph, END
from langgraph.prebuilt import ToolNode
from typing import TypedDict, List
from langchain_core.messages import AIMessage, HumanMessage
from langchain_google_genai import ChatGoogleGenerativeAI

# Shared LLM setup
llm = ChatGoogleGenerativeAI(
        model="gemini-2.0-flash-thinking-exp-01-21",
        temperature=0.2
    )

# Define state structure
class ReviewState(TypedDict):
    proposal: str
    legal_feedback: str
    ethics_feedback: str
    policy_feedback: str
    technical_analyst_feedback: str
    final_verdict: str

# Define agents
def legal_advisor(state: ReviewState) -> ReviewState:
    msg = f"As a legal advisor, evaluate the following proposal for legality:\n\n{state['proposal']}, follow the Indian Penal Code(IPC) list out the issues and you can try to modify the proposal accordingly to suit for legal stuff"
    response = llm.invoke(msg).content
    state["legal_feedback"] = response
    return state

def ethics_expert(state: ReviewState) -> ReviewState:
    msg = f"As an ethics expert, assess the following proposal for ethical issues:\n\n{state['proposal']}"
    response = llm.invoke(msg).content
    state["ethics_feedback"] = response
    return state

def policy_analyst(state: ReviewState) -> ReviewState:
    msg = f"As a public policy analyst, provide your opinion on the social and political risks of this proposal:\n\n{state['proposal']}"
    response = llm.invoke(msg).content
    state["policy_feedback"] = response
    return state

def technical_analyst(state: ReviewState) -> ReviewState:
    msg = f"As a public policy analyst, provide your opinion on of technical feasibility, challenges, and any known limitations of the proposal :\n\n{state['proposal']}"
    response = llm.invoke(msg).content
    state["policy_feedback"] = response
    return state


def final_verdict(state: ReviewState) -> ReviewState:
    summary_prompt = (
        f"Summarize the following feedback from the board and give a final verdict:\n\n"
        f"Legal Advisor: {state['legal_feedback']}\n\n"
        f"Ethics Expert: {state['ethics_feedback']}\n\n"
        f"Policy Analyst: {state['policy_feedback']}\n\n"
        f"Is the deployment advisable? Provide a rationale."
    )
    response = llm.invoke(summary_prompt).content
    state["final_verdict"] = response
    return state

# Build LangGraph
builder = StateGraph(ReviewState)

builder.add_node("legal_advisor", legal_advisor)
builder.add_node("ethics_expert", ethics_expert)
builder.add_node("policy_analyst", policy_analyst)
builder.add_node("final_verdict", final_verdict)

builder.set_entry_point("legal_advisor")

# Parallel paths
builder.add_edge("legal_advisor", "ethics_expert")
builder.add_edge("ethics_expert", "policy_analyst")
builder.add_edge("policy_analyst", "final_verdict")
builder.add_edge("final_verdict", END)

# Compile
graph = builder.compile()

# Run!
if __name__ == "__main__":
    user_input = """
    We want to deploy an AI system in public schools that uses students' webcam footage during online exams to 
    detect facial expressions and predict cheating behavior. The system flags suspicious behavior for review 
    by school authorities.
    """

    initial_state = {"proposal": user_input}
    result = graph.invoke(initial_state)

    print("\n🧾 Final Verdict:\n", result["final_verdict"])
