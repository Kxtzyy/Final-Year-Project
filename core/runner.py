from agents.coding_team import create_coding_team
from autogen_agentchat.messages import TextMessage
import asyncio
import sys

async def run_task_stream(task: str):
    team = create_coding_team()
    async for message in team.run_stream(task=task):
        if isinstance(message, TextMessage):
            sys.stdout.write("\r" + " " * 20 + "\r")
            sys.stdout.flush()
            print(f"\n[{message.source}]\n")
            for char in message.content:
                print(char, end="", flush=True)
                await asyncio.sleep(0.02)  # adjust speed here
            print("\n" + "-" * 60)
        sys.stdout.write("Thinking...")
        sys.stdout.flush()