from typing import TypedDict
from langgraph.graph import StateGraph, START, END

# define the state structure using TypedDict
class MyState(TypedDict):
    name: str

# 1st node function - add Mr.
def add_mr(state: MyState) -> MyState:
    current_name = state["name"]
    updated_name = "Mr. " + current_name
    return {"name" : updated_name}

# 2nd node function - add Welcome message
def add_welcome(state: MyState) -> MyState:
    current_name = state["name"]
    updated_name = current_name + " - Welcome!"
    return {"name" : updated_name}

# create a state graph
workflow = StateGraph(MyState)

# add nodes to the graph
workflow.add_node("node_mr", add_mr)
workflow.add_node("node_welcome", add_welcome)

# edges: START -> node_mr -> node_welcome -> END
workflow.add_edge(START, "node_mr")
workflow.add_edge("node_mr", "node_welcome")
workflow.add_edge("node_welcome", END)

# compile the graph into an executable app
app = workflow.compile()

# graph running with input data
result = app.invoke({"name": "Ganesh"})

# print the result
print(result)

# print the graph structure in ASCII format
print(app.get_graph().draw_ascii())