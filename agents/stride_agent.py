from crewai import Agent, Task

from utils.config import build_new_llm_client
from utils.prompt_loader import load_prompt

def build_stride_agent_and_task():
    stride_agent = Agent(
        role="Senior Cloud Security Architect – STRIDE Threat Modeling Specialist",
        goal=(
            "Identify STRIDE threats for each EXISTING component and communication flow "
            "based strictly on exposure, trust boundaries, and data flows"
        ),
        backstory=load_prompt("stride.md"),
        verbose=True,
        llm=build_new_llm_client(0.1),
        allow_delegation=False
    )

    return Task(
        description=(
            "You will receive a consolidated JSON containing:\n"
            "- All identified components\n"
            "- Their trust zones and exposure\n"
            "- All communication flows\n\n"
            "Your task is to identify ALL applicable STRIDE threats.\n\n"
            "Rules:\n"
            "- Do NOT create or modify components\n"
            "- Do NOT propose mitigations\n"
            "- Do NOT assume security controls\n"
            "- Threats MUST reference existing component IDs or flow IDs only\n"
            "- Every threat MUST include justification based on context\n\n"
            "Return ONLY valid JSON."
        ),
        expected_output=(
            "JSON containing a complete list of STRIDE threats mapped to "
            "component IDs and/or communication flows"
        ),
        agent=stride_agent
    )
