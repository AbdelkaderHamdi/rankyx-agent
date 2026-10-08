import os
from dotenv import load_dotenv
from langchain_groq import ChatGroq
from tavily import TavilyClient
from scrapegraph_py import ScrapeGraphAI

load_dotenv()

GROQ_API_KEY = os.getenv("GROQ_API_KEY")
TAVILY_API_KEY = os.getenv("TAVILY_API_KEY")
SGAI_API_KEY = os.getenv("SGAI_API_KEY")

MODEL_NAME = "qwen/qwen3.8-27b"  # check this name on Groq
OUTPUT_DIR = "./ai-agent-output"
os.makedirs(OUTPUT_DIR, exist_ok=True)

llm = ChatGroq(model=MODEL_NAME, api_key=GROQ_API_KEY, temperature=0)
search_client = TavilyClient(api_key=TAVILY_API_KEY)
scrape_client = ScrapeGraphAI(api_key=SGAI_API_KEY)