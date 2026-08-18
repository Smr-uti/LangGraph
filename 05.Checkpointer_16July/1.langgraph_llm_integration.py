# import necessary libraries
from typing_extensions import TypedDict
from langgraph.graph import StateGraph, START, END, MessagesState
from langchain_groq import ChatGroq
from pydantic import SecretStr
from langchain_core.messages import (HumanMessage,)
from dotenv import load_dotenv

load_dotenv()

llm=ChatGroq(model="llama-3.3-70b-versatile")

# class MessagesState(TypedDict):
#     messages: Annotated[list[AnyMessage], add_messages]

def node1(state:MessagesState):
    msg=state["messages"]
    response=llm.invoke(msg[-1].content)
    return {"messages":[response]}

workflow=StateGraph(MessagesState)

workflow.add_node("node1",node1)

workflow.add_edge(START,"node1")
workflow.add_edge("node1",END)

app=workflow.compile()

def interact_agent():
    while True:
        user_input=input("You:")
        if user_input.lower() in ["exit","quit"]:
            print("Conversation is ending:")
            break
        input_variable={
            "messages":[("human",user_input)]
        }
        for chunk in app.stream(input_variable,stream_node="values"): # type: ignore[arg-type]
            chunk["messages"][-1].pretty_print()
        # for chunk in app.stream(input_variable, stream_mode="values"):
        #     print(type(chunk["messages"]))
        #     print(chunk["messages"])


interact_agent()