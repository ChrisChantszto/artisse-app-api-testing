import pytest
from fastapi.testclient import TestClient
from unittest.mock import patch
from artisse-app-api.src.main import app  # assuming your FastAPI application is named as 'app' in 'main.py'
from artisse-app-api.src.notification.schemas import CreateNotificationRequest, NotificationHistory
from datetime import datetime

client = TestClient(app)

@patch('src.notification.services.create_new_push_notification')
def test_send_new_push_notification(mock_create_new_push_notification):
    new_notification = CreateNotificationRequest(
        user_id="test-user-id",
        type="test-type",
    )
    mock_create_new_push_notification.return_value = 1
    response = client.post("/notification", json=new_notification.dict())
    assert response.status_code == 200
    assert response.json()["message"] == "Send notification successfully"


@patch('src.notification.services.get_all_notification_history')
@patch('src.notification.services.get_inactive_notification_history')
def test_get_notification_history(mock_get_all_notification_history, mock_get_inactive_notification_history):
    # Assuming there is a user with id 'test-user-id' logged in
    mock_get_all_notification_history.return_value = [
        NotificationHistory(
            id=1,
            user_id="test-user-id",
            notification_type="test-type",
            notification_time=datetime.now(),
            active=True
        )
    ]
    mock_get_inactive_notification_history.return_value = []
    response = client.get("/notification/history", headers={"Authorization": "Bearer test-user-id"})
    assert response.status_code == 200
    assert response.json()["message"] == "Payment order created."


@patch('src.notification.services.activiate_notification_history')
def test_activate_individual_notification(mock_activiate_notification_history):
    # Assuming there is a user with id 'test-user-id' logged in and a history with id 'test-history-id'
    mock_activiate_notification_history.return_value = None
    response = client.put("/notification/history/test-history-id", headers={"Authorization": "Bearer test-user-id"})
    assert response.status_code == 200
    assert response.json()["message"] == "active notification success"


@patch('src.notification.services.activiate_notification_history')
def test_activate_all_notification_history(mock_activiate_notification_history):
    # Assuming there is a user with id 'test-user-id' logged in
    mock_activiate_notification_history.return_value = None
    response = client.post("/notification/history/all", headers={"Authorization": "Bearer test-user-id"})
    assert response.status_code == 201
    assert response.json()["message"] == "active notification success"