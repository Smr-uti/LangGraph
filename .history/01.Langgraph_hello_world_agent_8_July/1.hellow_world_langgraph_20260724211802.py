
from typing_extensions import TypedDict
from langgraph.graph import StateGraph,START,END

class GreetingState(TypedDict):
    greeting:str

def node1(state:GreetingState):
    state["greeting"]=state["greeting"]+" , How are you"
    return state 

builder=StateGraph(GreetingState)

builder.add_node("node1",node1)

builder.add_edge(START,"node1")
builder.add_edge("node1",END) 

result=graph.invoke({
    "greeting":"Good Morning"

})

print(result)