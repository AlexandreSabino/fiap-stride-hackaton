from crewai import Agent, Task
from crewai_tools import VisionTool

from domains.components import ArchitectureAnalysis
from utils.config import build_new_llm_client
from utils.prompt_loader import load_prompt


def build_auditor_agent_and_task(image_path, vision_task):
    vision_tool = VisionTool()

    audit_task_description = (
        f"1. Perform a meticulous reconciliation between the JSON output from 'vision_task' "
        f"and the physical pixels of the image located at: '{image_path}'.\n"
        "2. Execute the following 'High-Risk Area' checks:\n"
        "   - Quantitative Audit: Count every unique icon in the image. If the JSON count "
        "is lower, you MUST delegate back to the Analyst.\n"
        "   - Margin & Boundary Check: Scan the outer edges and sidebars for global services "
        "(Security, Logging, Messaging) that often lack direct flow arrows.\n"
        "   - Symmetry & Anomaly Check: Compare repetitive clusters (like Availability Zones). "
        "If one zone has a unique component not found in others, ensure it is captured.\n"
        "   - Path Continuity: Trace arrows from entry to exit. Ensure flows reach the "
        "data layer (Databases/Storage) and do not stop at the Load Balancer.\n"
        "3. If ANY component or flow is missing, delegate to the Analyst with specific "
        "spatial instructions (e.g., 'Check the bottom-right corner').\n"
        "4. Once the data is 100% verified, return ONLY the final JSON object."
    )

    auditor_agent = Agent(
        role="Cloud Architecture Quality Auditor",
        goal="Ensure the component inventory reflects 100% of the visual diagram through rigorous reconciliation.",
        backstory=load_prompt("auditor.md"),
        tools=[vision_tool],
        llm=build_new_llm_client(0.1),
        allow_delegation=True,
        verbose=True
    )

    return Task(
        description=audit_task_description,
        expected_output="A validated and complete ArchitectureAnalysis Pydantic object.",
        agent=auditor_agent,
        context=[vision_task],
        output_pydantic=ArchitectureAnalysis
    )