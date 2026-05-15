from agents.coding_team import create_coding_team
from autogen_agentchat.messages import TextMessage
from database import db
import asyncio
import sys

async def run_task_stream(task: str, conversation_id: int = None):

    # Initialise a fresh agent team for each request
    team = create_coding_team()
    
    output = []

    # Iterate over the stream, collecting only completed TextMessage objects
    async for message in team.run_stream(task=task):
        if isinstance(message, TextMessage):
            output.append(
                {
                    "agent": message.source,
                    "content": message.content
                }
            )
            
            # Persist each message to the database if a conversation ID was provided
            if conversation_id:
                await db.save_message(conversation_id, message.source, message.content)

    return output