from crewai import Agent, Task

from utils.config import build_new_llm_client
from utils.prompt_loader import load_prompt

def build_stride_agent_and_task(architecture_data):
    stride_agent = Agent(
        role="Senior Cloud Security Architect – STRIDE Threat Modeling Specialist",
        goal=(
            "Perform a deep STRIDE threat analysis on the provided architecture."
            "Identify STRIDE threats for each EXISTING component and communication flow "
            "based strictly on exposure, trust boundaries, and data flows"
        ),
        backstory=load_prompt("stride.md"),
        verbose=True,
        llm=build_new_llm_client(0.1),
        allow_delegation=False
    )

    return Task(
        description=f"Analyze the following architecture JSON and generate a STRIDE report: {architecture_data}",
        expected_output=(
            "A comprehensive Markdown report with threats and mitigations."
            "The report must be returned in markdown and PORTUGUESE LANGUAGE."
        ),
        agent=stride_agent
    )
