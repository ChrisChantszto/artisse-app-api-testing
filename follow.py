import unittest
from unittest.mock import patch
from fastapi.testclient import TestClient

from artisse_app_api.src.main import app
from artisse_app_api.src.follow.schemas import FollowUserRequest

client = TestClient(app)

class TestFollowAPI(unittest.TestCase):
    @patch('artisse_app_api.src.auth.dependencies.get_current_user')
    @patch('artisse_app_api.src.follow.services.create_follow_user')
    def test_follow_user(self, mock_create_follow_user, mock_get_current_user):
        # Define a sample user to follow
        user_to_follow = FollowUserRequest(user_id="followee_id")
        mock_create_follow_user.return_value = "follow_user_id"
        mock_get_current_user.return_value = "current_user_id"

        # Send POST request to /api/follow endpoint
        response = client.post("/api/follow", json=user_to_follow.dict())

        # Assert the status_code is 200 (as defined in your create_user_follow function)
        self.assertEqual(response.status_code, 200)

        # Assert the message returned
        self.assertEqual(response.json()['message'], 'Follow user successfully')

    @patch('artisse_app_api.src.auth.dependencies.get_current_user')
    @patch('artisse_app_api.src.follow.services.delete_follow_user')
    def test_unfollow_user(self, mock_delete_follow_user, mock_get_current_user):
        # Define a sample user to unfollow
        user_to_unfollow = FollowUserRequest(user_id="followee_id")
        mock_delete_follow_user.return_value = True
        mock_get_current_user.return_value = "current_user_id"

        # Send DELETE request to /api/follow endpoint
        response = client.delete("/api/follow", json=user_to_unfollow.dict())

        # Assert the status_code is 200 (as defined in your delete_user_follow function)
        self.assertEqual(response.status_code, 200)

        # Assert the message returned
        self.assertEqual(response.json()['message'], 'Follow removed from the follower list successfully')

    @patch('artisse_app_api.src.auth.dependencies.get_current_user')
    @patch('artisse_app_api.src.follow.services.create_follow_user')
    def test_follow_user_invalid_input(self, mock_create_follow_user, mock_get_current_user):
        # Define an invalid user to follow
        invalid_user_to_follow = FollowUserRequest(user_id="")
        mock_get_current_user.return_value = "current_user_id"
        mock_create_follow_user.side_effect = HTTPException(status_code=400, detail="Invalid user ID")

        # Send POST request to /api/follow endpoint
        response = client.post("/api/follow", json=invalid_user_to_follow.dict())

        # Assert the status_code is 400 (because of the invalid user ID)
        self.assertEqual(response.status_code, 400)

        # Assert the message returned
        self.assertEqual(response.json()['detail'], 'Invalid user ID')

    @patch('artisse_app_api.src.auth.dependencies.get_current_user')
    @patch('artisse_app_api.src.follow.services.delete_follow_user')
    def test_unfollow_user_invalid_input(self, mock_delete_follow_user, mock_get_current_user):
        # Define an invalid user to unfollow
        invalid_user_to_unfollow = FollowUserRequest(user_id="")
        mock_get_current_user.return_value = "current_user_id"
        mock_delete_follow_user.side_effect = HTTPException(status_code=400, detail="Invalid user ID")

        # Send DELETE request to /api/follow endpoint
        response = client.delete("/api/follow", json=invalid_user_to_unfollow.dict())

        # Assert the status_code is 400 (because of the invalid user ID)
        self.assertEqual(response.status_code, 400)

        # Assert the message returned
        self.assertEqual(response.json()['detail'], 'Invalid user ID')

if __name__ == "__main__":
    unittest.main()