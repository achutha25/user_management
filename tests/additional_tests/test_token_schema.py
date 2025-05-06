import pytest
from pydantic import ValidationError
from app.schemas.token_schema import TokenResponse

def test_token_response_valid():
    token = TokenResponse(access_token="abc.def.ghi")
    assert token.access_token == "abc.def.ghi"
    assert token.token_type == "bearer"  # default

def test_token_response_missing_access_token():
    with pytest.raises(ValidationError) as exc_info:
        TokenResponse()
    assert "field required" in str(exc_info.value)

def test_token_response_with_custom_type():
    token = TokenResponse(access_token="abc123", token_type="jwt")
    assert token.token_type == "jwt"

def test_token_response_example():
    example = TokenResponse.model_config["json_schema_extra"]["example"]
    token = TokenResponse(**example)
    assert token.access_token.startswith("eyJ")
    assert token.token_type == "bearer"

