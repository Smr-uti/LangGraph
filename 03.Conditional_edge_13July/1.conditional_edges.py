from typing_extensions import TypedDict
from langgraph.graph import StateGraph, START, END

class GreetingState(TypedDict):
    greeting:str

# Convert to lowercase
#output: good morning
def node1(state:GreetingState):
    state['greeting']=state['greeting'].lower()
    return state

# output: good morning, welcome to langchain
def node2(state:GreetingState):
    state['greeting']=state['greeting'] + ", Welcome to Langchain!"
    return state

# output: good morning, welcome to langgraph
def node3(state:GreetingState):
    state['greeting']=state['greeting'] + ", Welcome to LangGraph!"
    return state

# conditional node
def node4(state:GreetingState):
    if "good morning" in state['greeting']:
        return "node2"
    else: 
        return "node3"

# create graph
builder=StateGraph(GreetingState, input_schema=GreetingState, output_schema=GreetingState)

builder.add_node("node1", node1)
builder.add_node("node2", node2)
builder.add_node("node3", node3)
builder.add_node("node4", node4)

builder.add_edge(START, "node1")
builder.add_conditional_edges("node1", node4)
builder.add_edge("node2", END)
builder.add_edge("node3", END)

graph = builder.compile()

result = graph.invoke({
    "greeting":"GOOD MORNING"
})

print(result)

print(graph.get_graph().draw_ascii())
