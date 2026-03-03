from autogen_agentchat.agents import AssistantAgent
from autogen_agentchat.teams import RoundRobinGroupChat
from models.client import get_model_client

def create_coding_team():
    model_client = get_model_client()

    assistant   = AssistantAgent(name="assistant",   model_client=model_client, system_message="You are a helpful coding assistant. Write code to solve tasks. If given code to fix, keep track of the before and after and pass it along.")
    assistant_2 = AssistantAgent(name="assistant_2", model_client=model_client, system_message="Suggest an alternative way of solving the given task. If given code to fix, keep track of the before and after and pass it along.")
    assistant_3 = AssistantAgent(name="assistant_3", model_client=model_client, system_message="Evaluate the two suggestions and choose the better one. Choose the optimal solution, you are required to make a decision. Keep track of the before and after of the code after you have made a choice. Pass this along.")
    assistant_4 = AssistantAgent(name="assistant_4", model_client=model_client, system_message="Explain the code passed to you. If given a before and after, explain each change made.")

    return RoundRobinGroupChat(
        participants=[assistant, assistant_2, assistant_3, assistant_4],
        max_turns=4
    )