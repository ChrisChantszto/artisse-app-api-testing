import http from 'k6/http';
import { sleep } from 'k6';

const userCredentials = [
  { username: 'user1', password: 'password1' },
  { username: 'user2', password: 'password2' },
  // Add more test user credentials as needed
];

function obtainAuthTokens() {
  const loginUrl = 'https://your.api.endpoint/login';
  const tokens = [];

  for (const credentials of userCredentials) {
    const loginResponse = http.post(loginUrl, JSON.stringify(credentials), {
      headers: { 'Content-Type': 'application/json' },
    });

    const token = loginResponse.json().access_token;
    tokens.push(token);
  }

  return tokens;
}

const tokens = obtainAuthTokens(); // Obtain tokens for all test users

export const options = {
  // Configure the load test stages as needed
  stages: [
    { duration: '30s', target: 10 },
    { duration: '1m', target: 10 },
    { duration: '30s', target: 0 },
  ],
};

export default function () {
  const baseUrl = 'https://your.api.endpoint';
  const langCode = 'en'; // Replace with the desired language code

  // Randomly select a token for each request
  const token = tokens[Math.floor(Math.random() * tokens.length)];

  // Set up the request headers
  const headers = {
    'Content-Type': 'application/json',
    Authorization: `Bearer ${token}`,
  };

  // Send a POST request to the /train_images endpoint
  const trainImagesUrl = `${baseUrl}/train_images?lang_code=${langCode}`;
  const trainImagesData = {
    image_url_list: [
      'https://example.com/image1.jpg',
      'https://example.com/image2.jpg',
      // Add more image URLs as needed
    ],
  };
  http.post(trainImagesUrl, JSON.stringify(trainImagesData), { headers });

  // Send a POST request to the /upload_images endpoint
  const uploadImagesUrl = `${baseUrl}/upload_images`;
  const uploadImagesData = {
    // Add the necessary data for the /upload_images endpoint
  };
  http.post(uploadImagesUrl, JSON.stringify(uploadImagesData), { headers });

  sleep(1); // Wait 1 second between requests
}