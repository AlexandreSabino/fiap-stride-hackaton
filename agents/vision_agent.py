from crewai import Agent, Task
from crewai_tools import VisionTool

from domains.components import ArchitectureAnalysis
from utils.config import build_new_llm_client
from utils.prompt_loader import load_prompt


def build_vision_agent_and_task(image_path):
    vision_tool = VisionTool()

    vision_agent = Agent(
        role="Software Architecture Vision Analyst",
        goal="Extract a structured inventory of components and flows from diagrams.",
        backstory=load_prompt("vision.md"),
        verbose=True,
        llm=build_new_llm_client(0.1),
        tools=[vision_tool],
        allow_delegation=True
    )

    return Task(
        description=(
            f"Analyze the architecture diagram located at: '{image_path}'. "
            "Use the 'VisionTool' to read the image. "
            "CRITICAL: If a box contains multiple icons (e.g. Backend Systems containing SaaS and Web Services), "
            "you MUST create separate components for each internal icon. Do not group them."
            "Follow the scanning rules in your backstory strictly."
        ),
        expected_output="A structured Pydantic object containing components and flows.",
        agent=vision_agent,
        output_pydantic=ArchitectureAnalysis
    )