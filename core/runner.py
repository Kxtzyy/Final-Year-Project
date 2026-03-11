from agents.coding_team import create_coding_team
from autogen_agentchat.messages import TextMessage
import asyncio
import sys

async def run_task_stream(task: str):
    team = create_coding_team()
    
    output = []

    async for message in team.run_stream(task=task):
        if isinstance(message, TextMessage):
            output.append(
                {
                    "agent": message.source,
                    "content": message.content
                }
            )
    return output