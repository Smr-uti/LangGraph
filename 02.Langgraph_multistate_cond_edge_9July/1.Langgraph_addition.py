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

result=graph.invoke({
    "a":10,
    "b":20,
    "result":0
})

print(result)

print(graph.get_graph().draw_ascii())