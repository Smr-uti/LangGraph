from langchain_groq import ChatGroq
from langgraph.graph import StateGraph, START, END, MessagesState
from langchain_core.tools import tool
from langgraph.prebuilt import ToolNode
from dotenv import load_dotenv

@tool
# हवामानाची माहिती मिळवण्यासाठी tool define करतो
def fetch_weather_info(location:str):
    """
    This tool returns the weather information for a provided location
    """
    
     # Sample weather data dictionary मध्ये store केला आहे
    weather_info={
        "pune":"It's a raining outside, 20 degrees",
        "mumbai":"It's a 25 degrees and foggy",
        "nashik":"It's a 27 degree and cloudy"
    }
    # Location सापडल्यास weather info return कर अन्यथा default message return कर
    return weather_info.get(location, "weather info is not available for the provided location")

# Tool execute करण्यासाठी ToolNode तयार करत
tool_node=ToolNode([fetch_weather_info], handle_tool_errors=False)

# Groq LLM object तयार करतो
load_dotenv()

llm=ChatGroq(model="llama-3.3-70b-versatile").bind_tools([fetch_weather_info])
# bind_tools() मुळे LLM ला tool वापरता येत

def calling_llm(state:MessagesState):
    msg=state["messages"]
     # User चा शेवटचा message LLM ला पाठवत
    response=llm.invoke(msg[-1].content)
    # LLM response terminal मध्ये print करत
    print(response)
    # LLM ने tool call केला आहे का ते तपासत
    if response.tool_calls:
       # LLM ने मागितलेला tool execute करत
        tool_result=tool_node.invoke({"messages":[response]})

        # Tool चा output मिळवतो
        tool_message=tool_result["messages"][-1].content
         # Tool result response मध्ये add करत
        response.content=response.content+f"\n Tool result:{tool_message}" # type: ignore[operator]
    # Updated messages state मध्ये return करत
    return {"messages":[response]}

# MessagesState वापरून graph तयार करत
workflow=StateGraph(MessagesState)

# Graph मध्ये node add करत
workflow.add_node("calling_llm", calling_llm)

# Graph flow define करतो
# Graph सुरू झाल्यावर calling_llm node ला ज
workflow.add_edge(START, "calling_llm")
workflow.add_edge("calling_llm", END)

# Graph executable app मध्ये convert करत
app=workflow.compile()

def interact_agent():
     # सतत conversation चालू ठेवण्यासाठी loop
    while True:
        # User कडून input घ्
        user_input=input("You: ")
         # User ने exit किंवा quit लिहिल्यास conversation बंद कर
        if user_input.lower() in ["exit", "quit"]:
            print("conversation is ending...")
            break
         # Graph साठी input तयार करत
        input_variable={"messages":[("human", user_input)]}
        # Graph execute करून output stream कर
        for chunk in app.stream(input_variable, stream_mode="values"):  # type: ignore[arg-type]
            # AI चा response सुंदर format मध्ये print कर
            chunk["messages"][-1].pretty_print()

# Chat application सुरू कर
interact_agent()
