import os
from langchain_groq import ChatGroq
from langchain.agents import create_agent
from langgraph.checkpoint.memory import MemorySaver
from langchain_core.runnables.graph import MermaidDrawMethod, CurveStyle
from dotenv import load_dotenv
from display_graph import display_graph

# 1. Define Tool
def product_info(product_name: str) -> str:
    """Fetch product information."""

    product_catalog = {
        "iPhone 20": "The latest iPhone features an A15 chip and improved camera.",
        "MacBook": "The new MacBook has an M2 chip and a 14-inch Retina display.",
    }

    return product_catalog.get(
        product_name,
        "Sorry, product not found."
    )

# 2. Create Memory
checkpointer = MemorySaver()

# 3. Load Environment Variables
load_dotenv()

# 4. Create LLM
llm = ChatGroq(model="openai/gpt-oss-20b")

# 5. Create ReAct Agent
graph = create_agent(model=llm,tools=[product_info],checkpointer=checkpointer)

# 6. Visualise Graph
display_graph(graph,file_name=os.path.basename(__file__))

# 7. Save Graph as PNG
graph_png = graph.get_graph().draw_mermaid_png(draw_method=MermaidDrawMethod.API)

with open("react_agent_memory_graph.png", "wb") as f:
    f.write(graph_png)

print("Graph saved as: react_agent_memory_graph.png")

# 8. Thread Configuration
config = {"configurable": {"thread_id": "thread-1"}}

# 9. First User Input
inputs = {"messages": [("user","Hi, I'm James. Tell me about the new iPhone 20.")]}
messages = graph.invoke(inputs, config=config)

for message in messages["messages"]:
    message.pretty_print()

# 10. Second User Input
inputs2 = {"messages": [("user","Tell me more about the iPhone 20.")]}

messages2 = graph.invoke(inputs2, config=config)

for message in messages2["messages"]:
    message.pretty_print()