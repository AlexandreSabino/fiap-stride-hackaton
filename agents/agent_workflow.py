import json
import re

from crewai import Crew

from agents.context_agent import build_context_agent_and_task
from agents.stride_agent import build_stride_agent_and_task
from agents.vision_agent import build_vision_agent_and_task


def run_workflow(image_path):
    vision_output = identify_all_components(image_path)
    vision_output_json = extract_json(vision_output.raw)

    context_output = contextualize_components(vision_output_json, image_path)
    context_output_json = extract_json(context_output.raw)

    stride_output = stride_analyze(context_output_json, vision_output_json)
    stride_output_json = extract_json(stride_output.raw)

    return {
        'vision_output': vision_output_json,
        'context_output': context_output_json,
        'stride_output': stride_output_json,
    }


def extract_json(output):
    if isinstance(output, dict):
        return output

    if not isinstance(output, str):
        return output

    cleaned = re.sub(r"```json|```", "", output).strip()

    try:
        return json.loads(cleaned)
    except json.JSONDecodeError:
        raise ValueError(f"Invalid JSON returned by LLM:\n{output}")


def stride_analyze(vision_output, context_output):
    stride_analyze_task = build_stride_agent_and_task()
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
            "vision_output": vision_output,
            "context_output": context_output
        }
    )

def contextualize_components(vision_output, image_path):
    context_task = build_context_agent_and_task()
    crew = Crew(
        agents=[
            context_task.agent,
        ],
        tasks=[
            context_task,
        ],
        verbose=True
    )
    return crew.kickoff(
        inputs={
            "image_path": image_path,
            "vision_output": vision_output
        }
    )


def identify_all_components(image_path):
    vision_task = build_vision_agent_and_task()
    crew = Crew(
        agents=[vision_task.agent],
        tasks=[vision_task],
        verbose=True
    )
    return crew.kickoff(
        inputs={"image_path": image_path}
    )
