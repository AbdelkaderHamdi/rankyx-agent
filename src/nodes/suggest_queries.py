from src.config import llm
from src.schemas import State, SuggestedSearchQueries
from src.utils import save_json


def queries_node(state: State):
    i = state["inputs"]
    prompt = "\n".join([
        f"Rankyx is looking to buy {i['product_name']} at the best prices (value for price).",
        f"Target websites: {i['websites_list']}",
        f"The stores must sell the product in {i['country_name']}.",
        f"Generate at most {i['no_keywords']} queries, in {i['language']}.",
        "Queries must be varied and contain specific brands, types or technologies.",
        "Queries must reach a single-product ecommerce page, not a blog or listing.",
    ])
    result = llm.with_structured_output(SuggestedSearchQueries).invoke(prompt)
    queries = result.queries[: i["no_keywords"]]
    save_json("step_1_suggested_search_queries.json", {"queries": queries})
    return {"queries": queries}