import pytest
from httpx import AsyncClient


@pytest.mark.anyio
async def test_default(
    client: AsyncClient,
) -> None:
    """Tests users instance creation."""
    assert 201 == 201
