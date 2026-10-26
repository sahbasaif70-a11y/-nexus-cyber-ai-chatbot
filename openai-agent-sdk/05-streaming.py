import asyncio

from openai.types.responses import ResponseTextDeltaEvent
from dotenv import load_dotenv
from agents import Agents, Runner, trace
load_dotenv()
async def main();
    agent = Agent(
        name = "Travel Advisor",
        instructions="You Are a Travel advisor who gives short, enthusiastic recommendations for cities to visit. Keep responses to 2-3 sentences max.",
    )
    with trace(
        "Travel Recommendation",
    ):
        result = Runner.run_streamed(agent, "I have 5 days off and I love street food. Where should I go? Give me the city, the street food area and one must-try dish.")

    async for event in result.stream_events():
        if event.type == "raw response event" and isinstance(event.data).


