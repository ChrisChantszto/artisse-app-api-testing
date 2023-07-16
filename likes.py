# tests/test_likes_api.py

import pytest
import asynctest
from fastapi.testclient import TestClient
from httpx import AsyncClient
from artisse_app_api.src.main import app
from artisse_app_api.src.likes import services
from artisse_app_api.src.images import services as images_services
from artisse_app_api.src.auth.dependencies import get_current_user

@pytest.mark.asyncio
async def test_create_image_like():
    # Arrange
    image_id = "test_image"
    user_id = "test_user"
    like_image_id = "test_like_image_id"

    request_data = {
        "image_id": image_id
    }

    expected_response = {
        "status_code": 200,
        "message": "Image liked successfully",
        "data": like_image_id
    }

    get_current_user_mock = asynctest.CoroutineMock(return_value={"user_id": user_id})
    fetch_image_mock = asynctest.CoroutineMock(return_value={"share": True})
    create_like_image_mock = asynctest.CoroutineMock(return_value=like_image_id)

    app.dependency_overrides[get_current_user] = get_current_user_mock
    images_services.fetch_image = fetch_image_mock
    services.create_like_image = create_like_image_mock

    client = TestClient(app)

    # Act
    response = await client.post("/like_image", json=request_data)

    # Assert
    assert response.status_code == 200
    assert response.json() == expected_response
    fetch_image_mock.assert_awaited_once_with(image_id)
    create_like_image_mock.assert_awaited_once_with(like_image_id, user_id, image_id)


@pytest.mark.asyncio
async def test_delete_image_like():
    # Arrange
    image_id = "test_image"
    user_id = "test_user"

    request_data = {
        "image_id": image_id
    }

    expected_response = {
        "status_code": 200,
        "message": "Image removed from the like lists successfully"
    }

    get_current_user_mock = asynctest.CoroutineMock(return_value={"user_id": user_id})
    delete_like_image_mock = asynctest.CoroutineMock(return_value=True)

    app.dependency_overrides[get_current_user] = get_current_user_mock
    services.delete_like_image = delete_like_image_mock

    client = TestClient(app)

    # Act
    response = await client.delete("/like_image", json=request_data)

    # Assert
    assert response.status_code == 200
    assert response.json() == expected_response
    delete_like_image_mock.assert_awaited_once_with(user_id, image_id)
