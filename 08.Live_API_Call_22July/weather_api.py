import requests
from langgraph.graph import StateGraph, START, END, MessagesState

weather_api_key = c869d5d26d002bf0eb3ed625aaef032e

# Define the node to fetch live weather data
def live_weather_node(state):
    #Tell me the weather in pune
    user_query = state["messages"][-1].content
    city = user_query.split("in")[-1].strip()
    url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={weather_api_key}&units=metric"
    #http://api.openweathermap.org/data/2.5/weather?q=pune&appid=227fa444e2e7bbbe984f34122a9d6232&units=metric
    # Make the API call
    response = requests.get(url)
    print(response)
    if response.status_code == 200:
        data = response.json()
        print(data)
        temperature = data['main']['temp']
        description = data['weather'][0]['description']
        return {"messages": [f"The weather in {city} is {temperature}°C with {description}."]}
    else:
        return {"messages": ["Sorry, I couldn't fetch the weather information."]}
    
from langgraph.graph import StateGraph, MessagesState, START, END   

# Define the graph workflow
builder = StateGraph(MessagesState)

# Add the weather node
builder.add_node("live_weather_node", live_weather_node)

# Set up the edges
builder.add_edge(START, "live_weather_node")
builder.add_edge("live_weather_node", END)

# Compile the graph
app = builder.compile()

# Simulate interaction with the weather API
def simulate_interaction():
    input_message = {"messages": [("human", "Tell me the weather in nashik")]}
    
    # Process the input and stream the result
    for result in app.stream(input_message, stream_mode="values"):
        result["messages"][-1].pretty_print()

simulate_interaction()