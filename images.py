import pytest
from fastapi.testclient import TestClient
from artisse-app-api.src.main import app
from artisse-app-api.src.schemas import User

client = TestClient(app)


def test_get_template_image():
    response = client.get("/template_image/{test-id}")
    assert response.status_code == 200
    assert response.json()["message"] == "Image retrieved successfully"

def test_get_template_image_list():
    response = client.get("/template_image_list")
    assert response.status_code == 200
    assert response.json()["message"] == "Template images retrieved successfully"

def test_get_template_categories():
    response = client.get("/template_categories")
    assert response.status_code == 200
    assert response.json()["message"] == "Template categories fetched successfully"

def test_like_template_image():
    response = client.put("/like_template_image/{test-id}")
    assert response.status_code == 200
    assert response.json()["message"] == "Template image liked successfully"

def test_delete_liked_template_image():
    response = client.delete("/like_template_image/{test-id}")
    assert response.status_code == 200
    assert response.json()["message"] == "Template image removed from the liked list successfully"

def test_get_liked_template_image_list():
    response = client.get("/template_image_list/liked")
    assert response.status_code == 200
    assert response.json()["message"] == "Liked template images retrieved successfully"