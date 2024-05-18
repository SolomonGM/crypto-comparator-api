from fastapi.testclient import TestClient
from main import app
import pytest
import httpx
from unittest.mock import patch

client = TestClient(app)

@pytest.fixture(scope="module")
def mock_fetch_prices():
    with patch("main.fetch_prices") as mock:
        mock.return_value = None
        yield mock

def test_read_root():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "Crypto to Currency Comparator API"}

def test_compare_single_crypto(mock_fetch_prices):
    mock_fetch_prices.side_effect = lambda: {
        "bitcoin": 50000.00,
        "ethereum": 4000.00,
        "litecoin": 300.00,
        "bitcoin-cash": 600.00,
        "usdt": 1.00
    }

    response = client.get("/compare/bitcoin/usd")
    assert response.status_code == 200
    assert response.json() == {
        "crypto_id": "bitcoin",
        "fiat_currency": "usd",
        "value": "50000.00"
    }

def test_compare_multiple_cryptos(mock_fetch_prices):
    mock_fetch_prices.side_effect = lambda: {
        "bitcoin": 50000.00,
        "ethereum": 4000.00,
        "litecoin": 300.00,
        "bitcoin-cash": 600.00,
        "usdt": 1.00
    }

    response = client.get("/compare?crypto_ids=bitcoin,ethereum&fiat_currency=usd")
    assert response.status_code == 200
    assert response.json() == {
        "bitcoin": "50000.00",
        "ethereum": "4000.00"
    }

def test_compare_crypto_not_supported(mock_fetch_prices):
    response = client.get("/compare/doge/usd")
    assert response.status_code == 404
    assert response.json() == {"detail": "Crypto to Currency Comparator API"}

def test_compare_crypto_price_not_available(mock_fetch_prices):
    mock_fetch_prices.side_effect = lambda: {
        "bitcoin": 50000.00,
        "ethereum": None,
        "litecoin": 300.00,
        "bitcoin-cash": 600.00,
        "usdt": 1.00
    }

    response = client.get("/compare/ethereum/usd")
    assert response.status_code == 404
    assert response.json() == {"detail": "Price not available"}
