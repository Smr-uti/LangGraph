# Import necessary components
import operator
import os
import asyncio

from langgraph.graph import StateGraph, START, END
from langchain_community.tools.tavily_search import TavilySearchResults
from langchain_groq import ChatGroq
from langgraph.prebuilt import create_react_agent

from pydantic import BaseModel, Field
from typing import Annotated, List, Tuple, Union
from typing_extensions import TypedDict

from langchain_core.prompts import ChatPromptTemplate
from dotenv import load_dotenv

from display_graph import display_graph

# Load environment variables
load_dotenv()

# Tavily Tool
Tavily_tool = TavilySearchResults(max_results=3)

tools = [Tavily_tool]

# Prompt for ReAct Agent
prompt = ChatPromptTemplate.from_messages(
    [
        ("system", "You are a helpful assistant."),
        ("placeholder", "{messages}")
    ]
)

prompt.pretty_print()

# LLM
llm = ChatGroq(
    model="openai/gpt-oss-20b",
    temperature=0
)

# ReAct Agent
agent_executor = create_react_agent(
    llm,
    tools,
    prompt=prompt
)

# PLAN AND EXECUTE STATE
class PlanExecute(TypedDict):
    input: str
    plan: List[str]
    past_steps: Annotated[List[Tuple], operator.add]
    response: str

# PLAN SCHEMA
class Plan(BaseModel):

    steps: List[str] = Field(
        description="Numbered unique steps to follow, in order"
    )

# RESPONSE SCHEMA
class Response(BaseModel):

    response: str = Field(
        description="Response to user"
    )

# ACT SCHEMA
class Act(BaseModel):

    action: Union[Response, Plan] = Field(
        description=(
            "Action to perform. "
            "If you want to respond to the user, use Response. "
            "If you need to further work, use Plan."
        )
    )

# PLANNER PROMPT
planner_prompt = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            """
            For the given objective, come up with a simple
            step-by-step plan.

            The plan should contain individual tasks.

            Do not add unnecessary steps.

            The final step should produce the final answer.

            Make sure each step has all the information needed.
            """
        ),
        (
            "user",
            "{input}"
        ),
    ]
)

# PLANNER
planner = (
    planner_prompt
    | ChatGroq(
        model="openai/gpt-oss-20b",
        temperature=0
    ).with_structured_output(Plan)
)

# RE-PLANNER PROMPT
replanner_prompt = ChatPromptTemplate.from_template(
    """
    You are a re-planner.

    Check the original objective, current plan,
    and completed steps.

    Decide what should happen next.

    If more work is required:
    Return ONLY the remaining steps.

    If all work is complete:
    Return the final answer.

    Do not repeat completed steps.

    Original objective:
    {input}

    Current plan:
    {plan}

    Completed steps:
    {past_steps}
    """
)

# RE-PLANNER
replanner = (
    replanner_prompt
    | ChatGroq(
        model="openai/gpt-oss-20b",
        temperature=0
    ).with_structured_output(Act)
)

# EXECUTION STEP
async def execute_step(state: PlanExecute):

    plan = state["plan"]

    # If no plan is left
    if not plan:
        return {}

    # Take first task
    task = plan[0]

    # Convert complete plan into string
    plan_str = "\n".join(
        f"{i + 1}. {step}"
        for i, step in enumerate(plan)
    )

    task_formatted = f"""
For the following plan:

{plan_str}

You are responsible for executing this task:

{task}

Complete the task and return its result.
"""

    # Execute using ReAct Agent
    agent_response = await agent_executor.ainvoke(
        {
            "messages": [
                ("user", task_formatted)
            ]
        }
    )

    # Get final agent message
    result = agent_response["messages"][-1].content

    return {
        "past_steps": [
            (task, result)
        ]
    }

# PLANNING STEP
async def plan_step(state: PlanExecute):

    plan = await planner.ainvoke(
        {
            "input": state["input"]
        }
    )

    return {
        "plan": plan.steps
    }

# RE-PLANNING STEP
async def replan_step(state: PlanExecute):

    output = await replanner.ainvoke(state)

    # If final response is generated
    if isinstance(output.action, Response):

        return {
            "response": output.action.response
        }

    # If more steps are required
    else:

        return {
            "plan": output.action.steps
        }

# CONDITIONAL ROUTING
def should_end(state: PlanExecute):

    if state.get("response"):

        return END

    else:

        return "agent"

# BUILD WORKFLOW
workflow = StateGraph(PlanExecute)

# Add nodes
workflow.add_node(
    "planner",
    plan_step
)

workflow.add_node(
    "agent",
    execute_step
)

workflow.add_node(
    "replan",
    replan_step
)

# EDGES
workflow.add_edge(
    START,
    "planner"
)

workflow.add_edge(
    "planner",
    "agent"
)

workflow.add_edge(
    "agent",
    "replan"
)

workflow.add_conditional_edges(
    "replan",
    should_end,
    ["agent", END]
)

# COMPILE
app = workflow.compile()

# DISPLAY GRAPH
display_graph(
    app,
    file_name=os.path.basename(__file__)
)

# RUN PLAN AND EXECUTE
async def run_plan_and_execute():

    inputs = {
        "input":
        """
        Grace weighs 125 pounds.
        Alex weighs 2 pounds less than 4 times
        what Grace weighs.

        What are their combined weights in pounds?
        """
    }

    config = {
        "recursion_limit": 50
    }

    async for event in app.astream(
        inputs,
        config=config
    ):

        for k, v in event.items():

            if k != "__end__":

                print("\n==============================")
                print("NODE:", k)
                print("==============================")

                print(v)

# MAIN
if __name__ == "__main__":

    asyncio.run(
        run_plan_and_execute()
    )