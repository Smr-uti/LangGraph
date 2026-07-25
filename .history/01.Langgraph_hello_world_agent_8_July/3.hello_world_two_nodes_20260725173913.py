from typing_extensions import TypedDict
from langgraph.graph import StateGraph,START,END

class GreetingState(TypedDict):
    greeting:str
    sample_var:int

def node1(state:GreetingState):
    state["greeting"]=state["greeting"]+" , How are you?"
    state["sample_var"]=state["sample_var"]+1
    return state 

def node2(state:GreetingState):
    state["greeting"]=state["greeting"]+"!"
    return state

builder=StateGraph(GreetingState)

builder.add_node("node1",node1)
builder

builder.add_edge(START,"node1")
builder.add_edge("node1",END) 

graph=builder.compile()

result=graph.invoke({
    "greeting":"Good Morning",
    "sample_var":10

})

print(result)

# print(graph.get_graph().draw_ascii())

