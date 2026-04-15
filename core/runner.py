from agents.coding_team import create_coding_team
from autogen_agentchat.messages import TextMessage
from database import db
import asyncio
import sys

async def run_task_stream(task: str, conversation_id: int = None):
    print(f"conversation_id received: {conversation_id}")
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
            if conversation_id:
                await db.save_message(conversation_id, message.content)

    return output