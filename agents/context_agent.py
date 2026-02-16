from crewai import Agent, Task
from crewai_tools import VisionTool

from utils.config import build_new_llm_client
from utils.prompt_loader import load_prompt


def build_context_agent_and_task():
    vision_tool = VisionTool()
    context_agent = Agent(
        role="Senior Cloud Security Architect (Spatial & Trust Boundary Analyst)",
        goal="Derive trust zones, boundaries, and communication flows from architecture diagrams",
        backstory=load_prompt("context.md"),
        verbose=True,
        llm=build_new_llm_client(0.1),
        tools=[vision_tool],
        allow_delegation=False
    )
    return Task(
        description=(
            "You will receive:\n"
            "1. The FULL JSON output of the Vision Analysis Agent containing ALL component IDs\n"
            "2. The architecture diagram image at path '{image_path}'\n\n"
            "Your task is to analyze ONLY spatial relationships, trust boundaries, and "
            "communication flows.\n"
            "You MUST NOT create, remove, rename, or reclassify components.\n"
            "You MUST reference ONLY existing component IDs."
        ),
        expected_output="JSON with trust zones, spatial context, and communication flows",
        agent=context_agent
    )
