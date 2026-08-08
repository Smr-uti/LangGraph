from typing_extensions import TypedDict
from langgraph.graph import StateGraph, START, END

#Input state -> only user input
class InputState(TypedDict):
    name: str

# Overall state -> shared between nodes
class OverallState(TypedDict):
    name: str 
    greeting_message: str

# Private state -> intermediate state not exposed outside
class PrivateState(TypedDict):
    final_private_message: str

# Output state ->Final result
class OutputState(TypedDict):
    final_message: str

# Node1 - create greeting message
def node1(state:InputState)->OverallState:
    greeting_added ="Hello" + state["name"]
    state["greeting_message"]=greeting_added
    return state

builder = StateGraph(input=InputState, output=OverallState)

