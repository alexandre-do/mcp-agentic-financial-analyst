import pathlib
from IPython.display import display, Image
from langgraph.graph.state import CompiledStateGraph


def print_graph(graph: CompiledStateGraph, save_name: str = None):
    if save_name:
        if ".png" not in save_name:
            save_name = save_name.split(".")[0] + ".png"
        pathlib.Path(save_name).write_bytes(graph.get_graph().draw_mermaid_png())
    display(Image(graph.get_graph().draw_mermaid_png()))
