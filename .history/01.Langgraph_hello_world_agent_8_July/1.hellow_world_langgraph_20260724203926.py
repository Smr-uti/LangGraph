from typing_extensions import TypedDict

class GreetingState(TypedDict):
    greeting:str

def node1(state:GreetingState):
    state["greeting"]=s