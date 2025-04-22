// app.js
// Ollama Web Interface - 메인 서버 파일

const express = require('express');
const path = require('path');
const axios = require('axios'); // ✅ axios 추가

const app = express();
const PORT = 8000;

// 1. 미들웨어
app.use(express.json());
app.use(express.urlencoded({ extended: true }));

// 2. 정적 파일 서빙 (public 폴더)
app.use(express.static(path.join(__dirname, 'public')));

// 3. 뷰 엔진 설정 (HTML 렌더링)
app.set('public', path.join(__dirname, 'public'));
app.set('view engine', 'html');
app.engine('html', require('ejs').renderFile);

// 4. API 프록시 (FastAPI -> /api/forecast)
app.get('/api/forecast', async (req, res) => {
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

// 5. 기타 라우터 (선택적으로 mainRouter 연결)
const mainRouter = require('./node-server/mainController');
app.use('/', mainRouter);

// 6. 서버 실행
app.listen(PORT, () => {
  console.log(`🚀 Ollama Web Interface server running at http://localhost:${PORT}`);
});
