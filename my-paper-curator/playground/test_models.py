import pytest
from pydantic import ValidationError


from playground.models import Paper, SearchRequest, SearchSettings, base_arxiv_id


def test_paper_defaults():
    paper = Paper(arxiv_id="1706.03762", title="Attention is all you need")
    assert paper.authors == []
    assert paper.citation_count == 0

def test_search_request_defaults():
    request = SearchRequest(query="transformers")
    assert request.size == 10
    assert request.use_hybrid is True
    assert request.categories is None

def test_paper_rejects_bad_arxiv_id():
    with pytest.raises(ValidationError):
        Paper(arxiv_id="not-an-id", title="Something")


@pytest.mark.parametrize("bad", [{"query": ""}, {"query": "x", "size": 0}, {"query": "x", "size": 51}])
def test_search_request_validation(bad):
    with pytest.raises(ValidationError):
        SearchRequest(**bad)


def test_search_settings_is_a_plain_dataclass():
    settings = SearchSettings(base_url="http://localhost:8000")
    assert settings.timeout_seconds == 30.0


def test_base_arxiv_id():
    assert base_arxiv_id("2609.30558v2") == "2609.30558"
    assert base_arxiv_id(" 2609.30558 ") == "2609.30558"