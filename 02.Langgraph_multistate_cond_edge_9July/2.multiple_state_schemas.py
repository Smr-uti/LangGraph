from typing_extensions import TypedDict
from langgraph.graph import StateGraph, START, END

# Input state -> only user input
class InputState(TypedDict):
    name:str

# Overall state -> shared between nodes
class OverallState(TypedDict):
    name:str
    greeting_message:str

# Private state -> intermediate state (not exposed outside)
class PrivateState(TypedDict):
    final_private_message:str

# Output State -> Final result
class OutputState(TypedDict):
    final_message:str

# Node1 - create greeting message
def node1(state: InputState) -> OverallState:
    greeting_added = "Hello " + state["name"]
    return {
        "name": state["name"],
        "greeting_message": greeting_added
    }

# Node2 - add welcome message
def node2(state: OverallState) -> PrivateState:
    add_welcome = state["greeting_message"] + " Welcome to Langgraph!"
    return {
        "final_private_message": add_welcome
    }

# Node3 - final message creation
def node3(state: PrivateState) -> OutputState:
    final_msg = state["final_private_message"] + " How are you?"
    return {
        "final_message": final_msg
    }
builder = StateGraph(OverallState, PrivateState, input_schema=InputState, output_schema=OutputState)

builder.add_node("node1", node1)
builder.add_node("node2", node2)
builder.add_node("node3", node3)

builder.add_edge(START, "node1")
builder.add_edge("node1", "node2")
builder.add_edge("node2", "node3")
builder.add_edge("node3", END)

graph=builder.compile()

result=graph.invoke({
    "name":"ganesh"
})

print(result)

print(graph.get_graph().draw_ascii())