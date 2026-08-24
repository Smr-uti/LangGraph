import os
from langchain_groq import ChatGroq
from dotenv import load_dotenv
from display_graph import display_graph
from langchain.agents import create_agent


# Define tools
def add(a: int, b: int) -> int:
    """Add two numbers together."""
    return a + b

def multiply(a: int, b: int) -> int:
    """Multiply two numbers together."""
    return a * b

def divide(a: int, b: int) -> float:
    """Divide a and b.

    Args:
        a: first int
        b: second int
    """
    return a / b

tools = [add, multiply,divide]

# Initialize the LLM
load_dotenv()

llm=ChatGroq(model="openai/gpt-oss-20b")
# Create the ReAct agent
graph = create_agent(model=llm, tools=tools)

#Visualise the graph
display_graph(graph,file_name= os.path.basename(__file__))

# User input
inputs = {"messages": [("user", "multiply 2 and 3 and add this result to 10")]}

# Run the ReAct agent
messages = graph.invoke(inputs)
for message in messages["messages"]:
    message.pretty_print()