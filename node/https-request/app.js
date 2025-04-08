const http = require('http');

const data = JSON.stringify({ todo : 'Buy the milk' });

const options = {
    hostman: '192.168.1.44',
    port: 8000,
    path: '/hello',
    method: 'GET'
};

const req = http.request(options, (res) => {
    console.log(`statusCode : ${res.statusCode}`);
    res.on('data', d => {
        process.stdout.write(d);
    });
});

req.on('error', error => {
    console.log(error);
});

req.write(data);
req.end();