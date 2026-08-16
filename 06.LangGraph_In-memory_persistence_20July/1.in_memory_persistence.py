from langchain_groq  import ChatGroq
from langgraph.graph import StateGraph, START, END, MessagesState
from langgraph.checkpoint.memory import MemorySaver
from dotenv import load_dotenv
import os

load_dotenv()

llm=ChatGroq(model="llama-3.3-70b-versatile")

def node1(state:MessagesState):
    msg=state["messages"]
    response=llm.invoke(msg)
    return {"messages":[response]}

workflow=StateGraph(MessagesState)

workflow.add_node("node1", node1)

workflow.add_edge(START, "node1")
workflow.add_edge("node1", END)

checkpointer=MemorySaver()

app=workflow.compile(checkpointer=checkpointer)

def interact_agent_across_session():
    while True:
        thread_id=input("Enter thread ID: (or 'new' for a new session):")
        if thread_id.lower() in ["exit", "quit"]:
            print("Conversation is ending...")
            break
        if thread_id.lower() == "new":
            thread_id=f"session_{os.urandom(4).hex()}"
            print(thread_id)

        while True:
                user_input=input("You:")
                if user_input.lower() in ["exit", "quit"]:
                    print("Conversation is ending:")
                    break
                input_variable={
                    "messages":[("human", user_input)]
                }
                config={
                    "configurable":{"thread_id":thread_id}
                }
                for chunk in app.stream(input_variable, stream_mode="values", config=config):
                    chunk["messages"][-1].pretty_print()
        
interact_agent_across_session()


