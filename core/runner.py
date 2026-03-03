from agents.coding_team import create_coding_team
from autogen_agentchat.messages import TextMessage

async def run_task_stream(task: str):
    team = create_coding_team()
    async for message in team.run_stream(task=task):
        if isinstance(message, TextMessage):
            print(f"[{message.source}]")
            print(message.content)
            print("-" * 60)