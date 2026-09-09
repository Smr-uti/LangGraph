import os
import subprocess
import sys
import random
from langchain_core.runnables.graph import MermaidDrawMethod, CurveStyle


def display_graph(graph, output_folder="output", file_name="graph"):

    # Code to visualize the graph, used across all lessons
    try:
        # First attempt: online Mermaid API (requires internet)
        mermaid_png = graph.get_graph(xray=1).draw_mermaid_png(
            draw_method=MermaidDrawMethod.API,
            curve_style=CurveStyle.NATURAL
        )
    except Exception as e:
        print(f"Failed to generate graph using Mermaid API ({e}).")
        print("Trying local (Pyppeteer) method instead...")
        try:
            mermaid_png = graph.get_graph(xray=1).draw_mermaid_png(
                draw_method=MermaidDrawMethod.PYPPETEER,
                curve_style=CurveStyle.NATURAL
            )
        except Exception as e2:
            print(f"Could not generate graph image: {e2}")
            print("Tip: try running 'pip install pyppeteer' and rerun.")
            return  # Image generation failed, so nothing more to do

    # Create output folder if it doesn't exist
    output_folder = "./output"
    os.makedirs(output_folder, exist_ok=True)

    filename = os.path.join(output_folder, f"{file_name}_{random.randint(1, 100000)}.png")
    with open(filename, 'wb') as f:
        f.write(mermaid_png)

    print(f"Graph saved at: {filename}")

    # Attempt to open the file (may fail in headless/server environments, so wrapped safely)
    try:
        if sys.platform.startswith('darwin'):
            subprocess.call(('open', filename))
        elif sys.platform.startswith('linux'):
            subprocess.call(('xdg-open', filename))
        elif sys.platform.startswith('win'):
            os.startfile(filename)
    except Exception as e:
        print(f"Could not auto-open the image, but the file is saved at: {filename} ({e})")