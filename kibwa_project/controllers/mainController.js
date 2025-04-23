const express = require('express');
const axios = require('axios');
const router = express.Router();

// 기본 페이지 테스트용
router.get('/', (req, res) => {
  res.send("Web Server Started...");
});

router.get('/hello', (req, res) => {
  res.send({ data: 'Hello World!!' });
});

// 1. 전기차 예측 FastAPI 연동
const forecastAPI = 'http://192.168.1.44:3000/r_forecast';
router.get('/forecast', async (req, res) => {
  const { sido, sigungu } = req.query;

  if (!sido || !sigungu) {
    return res.status(400).json({ result: false, message: 'sido와 sigungu는 필수입니다.' });
  }

  try {
    const response = await axios.get(forecastAPI, {
      params: { sido, sigungu }
    });
    res.json(response.data);
  } catch (err) {
    console.error('[FastAPI 호출 오류]:', err.message);
    res.status(500).json({ result: false, message: 'FastAPI 서버 호출 실패' });
  }
});


module.exports = router;
