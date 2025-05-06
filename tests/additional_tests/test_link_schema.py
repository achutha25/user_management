import pytest
from pydantic import ValidationError
from app.schemas.link_schema import Link


def test_valid_link_creation():
    link = Link(
        rel="self",
        href="https://api.example.com/qr/123",
        action="GET"
    )
    assert link.rel == "self"
    assert link.href == "https://api.example.com/qr/123"
    assert link.action == "GET"
    assert link.type == "application/json"  # default


def test_link_with_invalid_href():
    with pytest.raises(ValidationError) as exc_info:
        Link(
            rel="self",
            href="not-a-valid-url",
            action="GET"
        )
    assert "value is not a valid URL" in str(exc_info.value)


def test_link_schema_example():
    # Use the example directly from the schema config
    example = Link.model_config["json_schema_extra"]["example"]
    link = Link(**example)
    assert link.rel == "self"
    assert link.href == "https://api.example.com/qr/123"
    assert link.action == "GET"
    assert link.type == "application/json"

