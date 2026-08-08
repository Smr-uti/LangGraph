from typing import TypedDict
from langgraph.graph import StateGraph, START, END

# data structure for the state
class MathState(TypedDict):
    number : int

# node function to double the number in the state
def double_number(state: MathState) -> MathState:
    original_num = state["number"]
    doubled_num = original_num * 2
    return {"number": doubled_num}

# create the state graph
workflow = StateGraph(MathState)

# add the double_number node to the workflow
workflow.add_node("double_node", double_number)

# START -> double_node -> END
workflow.add_edge(START, "double_node")
workflow.add_edge("double_node", END)

# compile the workflow
app = workflow.compile()

print(app.get_graph().draw_ascii())

# run the workflow
result = app.invoke({"number" : 15})
print(result)



