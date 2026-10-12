
from pydantic import BaseModel, Field
from dataclasses import dataclass
import re

class Paper(BaseModel):
    arxiv_id: str = Field(description="The arXiv ID of the paper", pattern=r"^\d{4}\.\d{4,5}(v\d+)?$")
    title: str = Field(description="The title of the paper")
    authors: list[str] = Field(description="The authors of the paper", default =[])
    citation_count: int = Field(description="The citation count of the paper", default =0, ge=0)

class SearchRequest(BaseModel):
    query: str = Field(description="The query to search for papers", min_length=1, max_length=500)
    size : int = Field(description="The number of papers to return", default =10, ge=1, le=50)
    use_hybrid: bool = Field(description="Whether to use the hybrid search", default =True)
    categories: list[str] = Field(description="The categories to search for papers", default =None)

@dataclass
class SearchSettings:
    base_url: str
    timeout_seconds: float = 30.0

def base_arxiv_id(arxiv_id: str) -> str:
    # re.sub(r"v\d+$", "", text) replaces "v plus digits at the very end" with nothing. Call .strip() first.
    return re.sub(r"v\d+$", "", arxiv_id.strip())

