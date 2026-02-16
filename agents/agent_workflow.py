from crewai import Crew

from agents.auditor_agent import build_auditor_agent_and_task
from agents.stride_agent import build_stride_agent_and_task
from agents.vision_agent import build_vision_agent_and_task


def run_workflow(image_path):
    vision_output = identify_all_components(image_path)
    stride_output = stride_analyze(vision_output)

    return {
        'vision_output': vision_output,
        'stride_output': stride_output.raw,
    }


def stride_analyze(vision_output):
    stride_analyze_task = build_stride_agent_and_task(vision_output)
    crew = Crew(
        agents=[
            stride_analyze_task.agent,
        ],
        tasks=[
            stride_analyze_task
        ],
        verbose=True
    )
    return crew.kickoff(
        inputs={
            "vision_output": vision_output
        }
    )


def identify_all_components(image_path):
    vision_task = build_vision_agent_and_task(image_path)
    agent_auditor = build_auditor_agent_and_task(image_path, vision_task)

    crew = Crew(
        agents=[vision_task.agent, agent_auditor.agent],
        tasks=[vision_task, agent_auditor],
        verbose=True
    )
    result = crew.kickoff()
    architecture_data = result.pydantic
    return architecture_data.model_dump()
