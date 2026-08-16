from typing import TypedDict
from langgraph.graph import StateGraph, START, END

class Simple(TypedDict):
    message: str

def say_hello(state: Simple) -> Simple:
    new_message = "Hello " + state["message"]
    return {"message": new_message}

workflow = StateGraph(Simple)

workflow.add_node("greeter_node", say_hello)

workflow.add_edge(START, "greeter_node")
workflow.add_edge("greeter_node", END)

app = workflow.compile()

result = app.invoke({"message": "Ganesh"})

print(result)
