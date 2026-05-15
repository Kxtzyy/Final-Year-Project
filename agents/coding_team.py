from autogen_agentchat.agents import AssistantAgent
from autogen_agentchat.teams import RoundRobinGroupChat
from models.client import get_model_client

def create_coding_team():
    
    # Initialise the shared model client for all agents
    model_client = get_model_client()

    # First agent: produces an initial implementation of the coding task
    coder = AssistantAgent(
        name="Coder",
        model_client=model_client,
        system_message="""You are the first agent in a coding assistant pipeline.
        If the user input is not a coding-related task, respond politely explaining 
        that you are a coding assistant and cannot help with that request. Do not pass 
        anything further.
        If it is a coding task, write or edit the code to fulfil the request and pass 
        it to the next agent."""
    )

    # Second agent: produces an alternative implementation using a different approach
    alternative_coder = AssistantAgent(
        name="Alternative_Coder",
        model_client=model_client,
        system_message="""You are the second agent in a coding assistant pipeline.
        If the previous agent indicated the input was not a coding task, repeat their 
        response and do not continue.
        Otherwise, write an alternative implementation of the code produced by the 
        previous agent, using a different approach or method."""
    )

    # Third agent: compares both implementations and selects the stronger one
    reviewer = AssistantAgent(
        name="Reviewer",
        model_client=model_client,
        system_message="""You are the third agent in a coding assistant pipeline.
        If the previous agents indicated the input was not a coding task, repeat their 
        response and do not continue.
        Otherwise, compare both code versions produced by the previous agents. Choose 
        the better version and clearly explain your reasoning, considering readability, 
        efficiency and correctness."""
    )

    # Fourth agent: explains the chosen implementation line-by-line for beginners
    explainer = AssistantAgent(
        name="Explainer",
        model_client=model_client,
        system_message="""You are the final agent in a coding assistant pipeline.
        If the previous agents indicated the input was not a coding task, repeat their 
        response and do not continue.
        Otherwise, take only the chosen version of the code from the previous agent 
        and explain how it works line-by-line in plain English, suitable for a beginner 
        developer."""
    )

    # Orchestrate agents sequentially using RoundRobinGroupChat, one turn each
    return RoundRobinGroupChat(
        participants=[coder, alternative_coder, reviewer, explainer],
        max_turns=4
    )   