import os
import json
from src.config import llm, OUTPUT_DIR
from src.schemas import State


def report_node(state: State):
    prompt = "\n".join([
        "Generate a professional HTML page for a procurement report. Use Bootstrap CSS (CDN).",
        "Sections: 1. Executive Summary 2. Introduction 3. Methodology 4. Findings (tables)",
        "5. Analysis 6. Recommendations (rank products best to worst, with notes)",
        "7. Conclusion 8. Appendices.",
        "Return only the HTML, no markdown fences.",
        "Products JSON:",
        json.dumps(state["products"], ensure_ascii=False)[:12000],
    ])
    html = llm.invoke(prompt).content.strip()
    if html.startswith("```"):
        html = html.split("\n", 1)[1].rsplit("```", 1)[0]
    with open(os.path.join(OUTPUT_DIR, "step_4_procurement_report.html"), "w", encoding="utf-8") as f:
        f.write(html)
    return {"report_html": html}