import json
import pandas as pd
import streamlit as st
import streamlit.components.v1 as components

from src.graph import run_agent

st.set_page_config(page_title="Rankyx Procurement Agent", page_icon="🛒", layout="wide")
st.title("🛒 Rankyx Procurement Agent")
st.caption("Find the best products for your company and get a ready report.")

STEP_LABELS = {
    "queries": "Suggesting search queries",
    "search": "Searching the web",
    "scrape": "Extracting product data",
    "report": "Writing the report",
}

# ---------- Sidebar: inputs ----------
with st.sidebar:
    st.header("Your request")
    with st.form("inputs_form"):
        product_name = st.text_input("Product", placeholder="coffee machine for the office")
        websites_text = st.text_area(
            "Websites (one per line)",
            value="www.amazon.eg\nwww.jumia.com.eg\nwww.noon.com/egypt-en",
        )
        country_name = st.text_input("Country", value="Egypt")
        language = st.selectbox("Query language", ["English", "French", "Arabic", "Spanish", "German"])
        no_keywords = st.slider("Number of queries", 1, 10, 5)
        score_th = st.slider("Min relevance score", 0.0, 1.0, 0.10, 0.05)
        top_n = st.slider("Pages to scrape", 1, 20, 5)
        submitted = st.form_submit_button("🚀 Run agent", use_container_width=True)

# ---------- Run ----------
if submitted:
    websites = [w.strip() for w in websites_text.splitlines() if w.strip()]

    if not product_name.strip():
        st.error("Please enter a product name.")
    elif not websites:
        st.error("Please enter at least one website.")
    else:
        inputs = {
            "product_name": product_name.strip(),
            "websites_list": websites,
            "country_name": country_name.strip(),
            "no_keywords": no_keywords,
            "language": language,
            "score_th": score_th,
            "top_recommendations_no": top_n,
        }

        bar = st.progress(0.0)
        with st.status("Running agent...", expanded=True) as status:

            def on_progress(node, n, total):
                bar.progress(n / total)
                st.write(f"✅ Step {n}/{total}: {STEP_LABELS.get(node, node)}")

            try:
                st.session_state["result"] = run_agent(inputs, on_progress=on_progress)
                status.update(label="Done!", state="complete", expanded=False)
            except Exception as e:
                st.session_state.pop("result", None)
                status.update(label="Failed", state="error")
                st.error(f"Agent failed: {e}")

# ---------- Output ----------
result = st.session_state.get("result")

if not result:
    st.info("Fill the form on the left and click **Run agent**.")
else:
    products = result.get("products", [])
    c1, c2, c3 = st.columns(3)
    c1.metric("Queries", len(result.get("queries", [])))
    c2.metric("Search results", len(result.get("search_results", [])))
    c3.metric("Products extracted", len(products))

    tab_report, tab_products, tab_search, tab_dl = st.tabs(
        ["📄 Report", "📦 Products", "🔎 Queries & Search", "⬇️ Download"]
    )

    with tab_report:
        html = result.get("report_html", "")
        if html:
            components.html(html, height=900, scrolling=True)
        else:
            st.warning("No report was generated.")

    with tab_products:
        if not products:
            st.warning("No product could be extracted. Try more queries or a lower score.")
        else:
            df = pd.DataFrame([
                {
                    "Image": p.get("product_image_url"),
                    "Title": p["product_title"],
                    "Price": p["product_current_price"],
                    "Original price": p.get("product_original_price"),
                    "Discount %": p.get("product_discount_percentage"),
                    "Link": p.get("product_url") or p["page_url"],
                }
                for p in products
            ]).sort_values("Price")
            st.dataframe(
                df,
                use_container_width=True,
                hide_index=True,
                column_config={
                    "Image": st.column_config.ImageColumn("Image"),
                    "Link": st.column_config.LinkColumn("Link", display_text="Open"),
                },
            )
            with st.expander("Specifications"):
                for p in products:
                    st.markdown(f"**{p['product_title']}**")
                    specs = p.get("product_specs", [])
                    if specs:
                        st.table(pd.DataFrame(specs))
                    else:
                        st.caption("No specs found.")

    with tab_search:
        st.subheader("Generated queries")
        for q in result.get("queries", []):
            st.write(f"- {q}")
        st.subheader("Search results")
        sr = result.get("search_results", [])
        if sr:
            st.dataframe(
                pd.DataFrame(sr),
                use_container_width=True,
                hide_index=True,
                column_config={"url": st.column_config.LinkColumn("url")},
            )

    with tab_dl:
        st.download_button(
            "Download report (HTML)",
            data=result.get("report_html", ""),
            file_name="procurement_report.html",
            mime="text/html",
        )
        st.download_button(
            "Download products (JSON)",
            data=json.dumps(products, indent=2, ensure_ascii=False),
            file_name="products.json",
            mime="application/json",
        )
        if products:
            st.download_button(
                "Download products (CSV)",
                data=df.drop(columns=["Image"]).to_csv(index=False),
                file_name="products.csv",
                mime="text/csv",
            )