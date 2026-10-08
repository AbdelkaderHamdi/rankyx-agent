from typing import List, Optional, TypedDict
from pydantic import BaseModel, Field


class SuggestedSearchQueries(BaseModel):
    queries: List[str] = Field(..., min_length=1, max_length=10)


class ProductSpec(BaseModel):
    specification_name: str
    specification_value: str


class ExtractedProduct(BaseModel):
    page_url: str = ""
    product_title: str
    product_image_url: Optional[str] = None
    product_url: Optional[str] = None
    product_current_price: float
    product_original_price: Optional[float] = None
    product_discount_percentage: Optional[float] = None
    product_specs: List[ProductSpec] = []


class State(TypedDict, total=False):
    inputs: dict
    queries: List[str]
    search_results: List[dict]
    products: List[dict]
    report_html: str