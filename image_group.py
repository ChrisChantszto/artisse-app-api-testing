import unittest
from unittest.mock import patch, Mock
from fastapi.testclient import TestClient
from fastapi import HTTPException

from artisse_app_api.src.main import app

client = TestClient(app)

class TestImageGroupAPI(unittest.TestCase):
    @patch('artisse_app_api.src.image_group.services.fetch_image_group')
    @patch('artisse_app_api.src.image_group.services.fetch_image_group_associations')
    @patch('artisse_app_api.src.image_group.services.fetch_image_group_category')
    @patch('artisse_app_api.src.image_group.services.delete_image_group_associations_db')
    @patch('artisse_app_api.src.image_group.services.delete_image_group_db')
    @patch('artisse_app_api.src.auth.dependencies.get_current_user')
    def test_get_and_delete_image_group(
        self,
        mock_get_current_user,
        mock_delete_image_group_db,
        mock_delete_image_group_associations_db,
        mock_fetch_image_group_category,
        mock_fetch_image_group_associations,
        mock_fetch_image_group
    ):
        mock_get_current_user.return_value = {"user_id": "test_user_id"}
        mock_fetch_image_group.return_value = {"user_id": "test_user_id", "image_group_id": "test_image_group_id", "image_count": 2, "prompt": "test prompt", "created_date": "2023-07-18T00:00:00", "updated_date": "2023-07-19T00:00:00", "complete": False}
        mock_fetch_image_group_associations.return_value = [{"image_id": "image_id_1"}, {"image_id": "image_id_2"}]
        mock_fetch_image_group_category.return_value = {"category": "test_category"}

        # Test GET endpoint
        response = client.get("/image_group/test_image_group_id")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()['message'], 'Image group retrieved successfully')
        self.assertEqual(response.json()['data']['image_group_id'], 'test_image_group_id')

        # Test DELETE endpoint
        mock_delete_image_group_db.return_value = 1
        response = client.delete("/image_group/test_image_group_id")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()['message'], 'Image group deleted successfully')

        # Test failed DELETE endpoint
        mock_delete_image_group_db.return_value = 0
        response = client.delete("/image_group/test_image_group_id")
        self.assertEqual(response.status_code, 500)
        self.assertEqual(response.json()['message'], 'The deletion failed. Please try again.')

if __name__ == "__main__":
    unittest.main()