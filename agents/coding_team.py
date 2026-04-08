from autogen_agentchat.agents import AssistantAgent
from autogen_agentchat.teams import RoundRobinGroupChat
from models.client import get_model_client

def create_coding_team():
    model_client = get_model_client()

    assistant   = AssistantAgent(name="assistant",   model_client=model_client, system_message="You are part of a team of AI agents. Your task is to only write or edit code for the give task and pass it on to the next agent.")
    assistant_2 = AssistantAgent(name="assistant_2", model_client=model_client, system_message="You are part of a team of AI agents. Your task is to write or edit code in an alternative way and pass it on.")
    assistant_3 = AssistantAgent(name="assistant_3", model_client=model_client, system_message="You are part of a team of AI agents. Your task is to look at both versions of the code and choose the best version with reasoning as to why this was chosen. Then pass the version that was chosen along.")
    assistant_4 = AssistantAgent(name="assistant_4", model_client=model_client, system_message="You are part of a team of AI agents. Your task is to look at the final version of the code and explain it's working.")

    return RoundRobinGroupChat(
        participants=[assistant, assistant_2, assistant_3, assistant_4],
        max_turns=4
    )   