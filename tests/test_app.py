# tests/test_app.py

import pytest
from app import create_app


@pytest.fixture
def client():
    app = create_app("testing")
    app.config["TESTING"] = True

    with app.test_client() as client:
        yield client


def test_home_page(client):
    response = client.get("/")
    assert response.status_code == 200
    assert b"AQI" in response.data


def test_analysis_page(client):
    response = client.get("/analysis")
    assert response.status_code == 200


def test_predict_page_get(client):
    response = client.get("/predict")
    assert response.status_code == 200


def test_predict_page_post(client):
    response = client.post(
        "/predict",
        data={
            "pm25": 50,
            "pm10": 80,
            "no2": 20,
            "so2": 10,
            "co": 1,
            "o3": 30,
            "month": 5,
            "dayofweek": 2
        },
        follow_redirects=True
    )

    assert response.status_code == 200
