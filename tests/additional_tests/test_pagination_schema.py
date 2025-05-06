import pytest
from pydantic import ValidationError
from app.schemas.pagination_schema import Pagination, PaginationLink, EnhancedPagination


def test_valid_pagination_model():
    p = Pagination(
        page=1,
        per_page=10,
        total_items=50,
        total_pages=5
    )
    assert p.page == 1
    assert p.per_page == 10
    assert p.total_items == 50
    assert p.total_pages == 5


def test_pagination_link_valid():
    link = PaginationLink(rel="next", href="https://example.com/page/2")
    assert link.rel == "next"
    assert link.href == "https://example.com/page/2"
    assert link.method == "GET"  # default value


def test_pagination_link_invalid_href():
    with pytest.raises(ValidationError) as exc_info:
        PaginationLink(rel="next", href="not-a-url")
    assert "value is not a valid URL" in str(exc_info.value)


def test_enhanced_pagination_add_link():
    ep = EnhancedPagination(
        page=1, per_page=10, total_items=100, total_pages=10
    )
    assert ep.links == []
    ep.add_link("next", "https://example.com/page/2")
    assert len(ep.links) == 1
    assert ep.links[0].rel == "next"
    assert ep.links[0].href == "https://example.com/page/2"


def test_pagination_schema_example():
    example = Pagination.model_config["json_schema_extra"]["example"]
    p = Pagination(**example)
    assert p.page == 1
    assert p.per_page == 10
    assert p.total_items == 50
    assert p.total_pages == 5

