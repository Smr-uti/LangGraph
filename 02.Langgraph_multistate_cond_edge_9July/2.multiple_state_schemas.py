from typing_extensions import TypedDict
from langgraph.graph import StateGraph, START, END

# Input state -> only user input
class InputState(TypedDict):
    name:str

# Overall state -> shared between nodes
class OverallState(TypedDict):
    name:str
    greeting_message:str

# Private state ->intermediate state (not exposed outside)
class PrivateState(TypedDict):
    final_private_message:str

# Output State -> Final result
class OutputState(TypedDict):
    final_message:str

# Node1 - create greeting message
def node1(state:InputState)->OverallState:
    greeting_added= "Hello" + state["name"]
    state["greeting_message"]=greeting_added
    return state

builder=StateGraph(InputState, output=OverallState)

builder.add_node("node1",node1)

builder.add_edge(START, "node1")
builder.add_edge("node1", END)

graph=builder.compile()

result=graph.invoke({
    "name":"ganesh"
})

print(result)

print(graph.get_graph().draw_ascii())