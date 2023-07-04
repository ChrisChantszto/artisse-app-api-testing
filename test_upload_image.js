import http from 'k6/http';
import { check, sleep } from 'k6';
import { FormData } from 'https://jslib.k6.io/formdata/0.0.2/index.js';

export let options = {
    stages: [
        { duration: '30s', target: 10 }, // Ramp up to 10 users over 30 seconds
        { duration: '1m', target: 10 }, // 10 users for 1 minute
        { duration: '30s', target: 0 }, // Ramp down to 0 users over 30 seconds
    ],
};

function authenticate(username, password) {
    const url = 'http://localhost:8000/token';
    const body = JSON.stringify({
        username: username,
        password: password,
    });
    const params = {
        headers: {
            'Content-Type': 'application/json',
        },
    };

    const res = http.post(url, body, params);
    return JSON.parse(res.body).data.access_token;
}

export default function () {
    // Replace with valid credentials for your application
    const username = 'your_username';
    const password = 'your_password';

    const jwtToken = authenticate(username, password);

    const url = 'http://localhost:8000/upload_image';
    const image_type = 1;
    const file_path = './path/to/your/image.jpg';

    const form_data = new FormData();
    form_data.append('image_type', image_type);
    form_data.append('file', http.file(file_path, 'image.jpg'));

    const params = {
        headers: {
            'Content-Type': 'multipart/form-data; boundary=' + form_data.boundary,
            'Authorization': 'Bearer ' + jwtToken,
        },
    };

    const res = http.post(url, form_data.body(), params);
    check(res, {
        'status is 200': (r) => r.status === 200,
    });

    sleep(1);
}