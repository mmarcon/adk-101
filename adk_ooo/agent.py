import asyncio
from tensorlake.applications import Image, function, Logger
import os

AGENT_IMAGE = Image(name="python:3.13-slim").run("pip install google-adk google-adk[extensions] arize-otel arize-phoenix-otel openinference-instrumentation-google-adk")

logger = Logger.get_logger(module="tour_guide_agent")


@function(min_containers=1)
def get_location() -> dict:
    """Gets the user's current location.

    Returns:
        dict: status and location information.
    """
    return {
        "status": "success",
        "location": "Barcelona, Spain"
    }


@function(image=AGENT_IMAGE, secrets=["ANTHROPIC_API_KEY", "ARIZE_API_KEY"], min_containers=2)
def run_tour_guide_agent(query: str) -> str:
    """A retired tour guide agent with passion for history and culture."""
    from google.adk.agents import Agent
    from google.adk.runners import InMemoryRunner
    from google.adk.models.lite_llm import LiteLlm
    from google.genai.types import Content, Part
    from openinference.instrumentation.google_adk import GoogleADKInstrumentor
    from arize.otel import register

    tracer_provider = register(
        space_id = "U3BhY2U6MzU1NTI6U0l6WA==",
        api_key = os.getenv("ARIZE_API_KEY"),
        project_name = "tensorlake-agents",
    )

    GoogleADKInstrumentor().instrument(tracer_provider=tracer_provider)

    async def _run():
        model = LiteLlm(
            model='anthropic/claude-3-7-sonnet-20250219'
        )

        agent = Agent(
            name="adk_ooo",
            model=model,
            description="A retired tour guide with a passion for history and culture.",
            instruction="You are a retired tour guide with a passion for history and culture. You are given a user question and you need to answer it to the best of your knowledge. You like to throw in some spanish phrases here and there. You can use the get_location tool to get the location of the user.",
            tools=[get_location],
        )

        runner = InMemoryRunner(agent=agent, app_name="tour_guide_app")
        user_id = "local_user"
        session = await runner.session_service.create_session(
            user_id=user_id, app_name="tour_guide_app"
        )

        response_text = ""

        logger.info(f"Running tour guide agent for user {user_id} with query {query}")
        async for event in runner.run_async(
            user_id=user_id,
            session_id=session.id,
            new_message=Content(parts=[Part(text=query)]),
        ):
            if event.content and event.content.parts:
                for part in event.content.parts:
                    if part.text:
                        response_text += part.text

        return response_text

    return asyncio.run(_run())