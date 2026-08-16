from typing_extensions import Typed
from langgraph.graph import StateGraph,START,END

class GreetingState(TypedDict):
    greeting:str
    sample_var:int

def node1(state:GreetingState):
    state["greeting"]=state["greeting"]+" , How are you?"
    return state 

def node2(state:GreetingState):
    state["greeting"]=state["greeting"]+"!"
    return state

builder=StateGraph(GreetingState)

builder.add_node("node1",node1)
builder.add_node("node2",node2)

builder.add_edge(START,"node2")
builder.add_edge("node1","node1") 
builder.add_edge("node1",END)

graph=builder.compile()

result=graph.invoke({
    "greeting":"Good Morning",

})

print(result)

print(graph.get_graph().draw_ascii())

