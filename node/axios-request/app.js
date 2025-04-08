const axios = require('axios');

axios
    .get('http://localhost:8000/hello', {
        todo : 'Buy the milk'
    })
    .then(res => {
        console.log(`statusCode : ${res.status}`);
        console.log(res.data);
    })
    .catch(error => {
        console.log(error);
    })