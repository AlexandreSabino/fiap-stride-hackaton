from crewai import Agent, Task
from crewai_tools import VisionTool

from utils.config import build_new_llm_client
from utils.prompt_loader import load_prompt


def build_vision_agent_and_task():
    vision_tool = VisionTool()
    vision_agent = Agent(
        role="Software Architecture Vision Analyst",
        goal="Identify ALL components from software architecture diagrams",
        backstory=load_prompt("vision.md"),
        verbose=True,
        llm=build_new_llm_client(0),
        tools=[vision_tool],
        allow_delegation=False
    )
    return Task(
        description=(
            "Use the VisionTool to analyze the image specifically at this path: "
            "'{image_path}'. You must identify all components"
        ),
        expected_output="JSON with ALL components",
        agent=vision_agent
    )
