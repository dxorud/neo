const express = require('express');
const axios = require('axios');
const router = express.Router();

// 기본 라우트: 홈 페이지
router.get('/', (req, res) => {
  res.render('service'); // views/index.html 렌더링
});

// 전기차 예측 데이터 FastAPI 연동 (프록시)
router.get('/api/ev_forecast', async (req, res) => {
  const { sido, sigungu } = req.query;

  try {
    const response = await axios.get('http://localhost:3000/forecast', {
      params: { sido, sigungu }
    });
    res.json(response.data);
  } catch (err) {
    console.error('[FastAPI 호출 오류]:', err.message);
    res.status(500).json({ result: false, message: 'FastAPI 서버 오류' });
  }
});

module.exports = router;
