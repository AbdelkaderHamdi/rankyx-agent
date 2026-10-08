from src.config import search_client
from src.schemas import State
from src.utils import save_json


def search_node(state: State):
    i = state["inputs"]
    seen, results = set(), []
    for q in state["queries"]:
        try:
            resp = search_client.search(q, max_results=5)
        except Exception as e:
            print(f"search failed for '{q}': {e}")
            continue
        for r in resp.get("results", []):
            if r["score"] < i["score_th"] or r["url"] in seen:
                continue
            seen.add(r["url"])
            results.append({
                "title": r["title"],
                "url": r["url"],
                "content": r["content"][:300],
                "score": r["score"],
                "search_query": q,
            })
    results.sort(key=lambda x: x["score"], reverse=True)
    save_json("step_2_search_results.json", results)
    return {"search_results": results}