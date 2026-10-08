from src.config import scrape_client
from src.schemas import State, ExtractedProduct
from src.utils import save_json


def scrape_node(state: State):
    i = state["inputs"]
    products = []
    for r in state["search_results"][: i["top_recommendations_no"]]:
        try:
            resp = scrape_client.extract(
                website_url=r["url"],
                user_prompt="Extract the product details from the web page.",
                output_schema=ExtractedProduct,
            )
            data = resp.get("result") or {}
            data["page_url"] = r["url"]
            products.append(ExtractedProduct(**data).model_dump())
        except Exception as e:
            print(f"skip {r['url']}: {e}")
    save_json("step_3_search_results.json", products)
    return {"products": products}