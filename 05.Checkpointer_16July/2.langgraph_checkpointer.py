# Groq चा LLM वापरण्यासाठी ChatGroq import करत आहोत
from langchain_groq import ChatGroq

# StateGraph -> LangGraph workflow तयार करण्यासाठी
# START -> graph ची सुरुवात दर्शवतो
# END -> graph चा शेवट दर्शवतो
# MessagesState -> messages store करण्यासाठी predefined state
from langgraph.graph import StateGraph, START, END, MessagesState

# Graph ची state memory मध्ये save करण्यासाठी MemorySaver import करत आहोत
from langgraph.checkpoint.memory import MemorySaver

from dotenv import load_dotenv

load_dotenv()

llm=ChatGroq(model="llama-3.3-70b-versatile")

# हा graph मधील एक node आहे  # state मध्ये सध्या असलेली पूर्ण conversation मिळते
def node1(state:MessagesState):
    # state मधून "messages" काढत आहोत
    # यात user चे previous messages आणि conversation history असू शकते
    msg=state["messages"]
    # पूर्ण messages LLM ला देत आहोत LLM त्यावर response generate करत
    response=llm.invoke(msg)
    # LLM चा नवीन response state मध्ये "messages" म्हणून add करत आहोत
    return {"messages":[response]}

# MessagesState वापरून LangGraph workflow तयार करत आहोत
workflow=StateGraph(MessagesState)

# Graph मध्ये "node1" नावाचा node add करत आहोत
workflow.add_node("node1",node1)

# Graph चा flow define करत आहोत Graph सुरू झाल्यावर सर्वप्रथम "node1" execute होईल
workflow.add_edge(START, "node1")
workflow.add_edge("node1", END) #node1 execute झाल्यानंतर graph समाप्त होईल

# Graph ची state memory मध्ये save करण्यासाठी MemorySaver वापरत आहोत हा in-memory checkpointer आहे
checkpointer=MemorySaver()

# Workflow ला compile करत आहोत. checkpointer जोडल्यामुळे conversation ची state save होऊ शकते
app=workflow.compile(checkpointer=checkpointer)

def interact_agent():
    thread_id="session1"
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

interact_agent()