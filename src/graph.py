from langgraph.graph import StateGraph, START, END
from src.schemas import State
from src.nodes.suggest_queries import queries_node
from src.nodes.search import search_node
from src.nodes.scrape import scrape_node
from src.nodes.report import report_node

STEPS = ["queries", "search", "scrape", "report"]


def build_graph():
    g = StateGraph(State)
    g.add_node("queries", queries_node)
    g.add_node("search", search_node)
    g.add_node("scrape", scrape_node)
    g.add_node("report", report_node)
    g.add_edge(START, "queries")
    g.add_edge("queries", "search")
    g.add_edge("search", "scrape")
    g.add_edge("scrape", "report")
    g.add_edge("report", END)
    return g.compile()


app = build_graph()


def run_agent(inputs: dict, on_progress=None) -> dict:
    """Run the agent. on_progress(node_name, step_number, total_steps) is called after each node."""
    final = {"inputs": inputs}
    for n, chunk in enumerate(app.stream({"inputs": inputs}, stream_mode="updates"), 1):
        for node_name, update in chunk.items():
            final.update(update)
            if on_progress:
                on_progress(node_name, n, len(STEPS))
    return final