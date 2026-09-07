import os

from dotenv import load_dotenv
from langchain_groq import ChatGroq
from langchain.agents import create_agent

from display_graph import display_graph


# Load environment variables
load_dotenv()

# Tool 1: Get demand data
def get_demand_data(product_id: str) -> dict:
    """Get demand data for a product."""

    # Mock API
    return {
        "product_id": product_id,
        "demand_level": "low"
    }

# Tool 2: Get competitor pricing
def get_competitor_pricing(product_id: str) -> dict:
    """Get competitor price for a product."""

    # Mock API
    return {
        "product_id": product_id,
        "competitor_price": 95.0
    }

# List of tools
tools = [
    get_demand_data,
    get_competitor_pricing
]

# Initialize Groq LLM
GROQ_API_KEY = os.getenv("GROQ_API_KEY")

if not GROQ_API_KEY:
    raise ValueError(
        "GROQ_API_KEY not found. "
        "Please add GROQ_API_KEY to your .env file."
    )

model = ChatGroq(
    model="openai/gpt-oss-20b",
    api_key=GROQ_API_KEY
)

# Create ReAct Agent
graph = create_agent(
    model=model,
    tools=tools
)

# Visualize graph
display_graph(
    graph,
    file_name=os.path.basename(__file__)
)

# Initial messages
initial_messages = [
    ("system", "You are an AI agent that dynamically adjusts product prices based on market demand and competitor prices."),
    ("user", "What should be the price for product ID '12345'?")
]

# Input for agent
inputs = {
    "messages": initial_messages
}

# Run the ReAct agent

for state in graph.stream(
    inputs,
    stream_mode="values"
):

    message = state["messages"][-1]

    if isinstance(message, tuple):
        print(message)
    else:
        message.pretty_print()