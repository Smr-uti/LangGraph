from typing_extensions import TypedDict
from langgraph.graph import StateGraph, START, END

# Define the state
class addition_state(TypedDict):
    a:int
    b:int
    result:int

# Define node function
def node1(state:addition_state):
    state['result']=state['a']+state['b']
    return state

# Initialize the graph and add nodes
workflow= StateGraph(addition_state)

workflow.add_node("node1",node1)

# update edges
workflow.add_edge(START,"node1")
workflow.add_edge("node1",END)

# compile and run the graph
graph=workflow.compile()

num1=int(input("Enter first number: "))
num2=int(input("Enter second number: "))

result=graph.invoke({
    "a":num1,
    "b":num2,
    "result":0
})

print(result)

print(graph.get_graph().draw_ascii())




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

builder.add_node("node1", node1)

builder.add_edge(START, "node1")
builder.add_edge("node1", END)

graph=builder.compile()

graph.invoke({
    "name":"Ganesh"
})

print(result)