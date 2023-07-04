import http from 'k6/http';
import { sleep } from 'k6';

export const options = {
  stages: [
    { duration: '30s', target: 10 }, // Ramp up to 10 virtual users over 30 seconds
    { duration: '1m', target: 10 }, // Maintain 10 virtual users for 1 minute
    { duration: '30s', target: 0 }, // Ramp down to 0 virtual users over 30 seconds
  ],
};

export default function () {
  // Replace with your API endpoint
  const baseUrl = 'https://your.api.endpoint';
  const url = `${baseUrl}/train_images`;

  // Replace with authentication token or credentials
  const token = 'your_auth_token';

  // Replace with request data
  const data = {
    image_url_list: [
      'https://example.com/image1.jpg',
      'https://example.com/image2.jpg',
      // Add more image URLs as needed
    ],
  };

  // Set up the request headers
  const headers = {
    'Content-Type': 'application/json',
    Authorization: `Bearer ${token}`,
  };

  // Send a POST request to the API
  http.post(url, JSON.stringify(data), { headers });

  sleep(1); // Wait 1 second between requests
}