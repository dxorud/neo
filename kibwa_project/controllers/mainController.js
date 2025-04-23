const express = require('express');
const axios = require('axios');
const router = express.Router();

// 기본 페이지
router.get('/', (req, res) => {
  res.render('index');  // 기본 페이지를 index.html로 설정
});

// 화면 렌더링
router.get('/data', (req, res) => {
  res.render('data');   // views/data.html
});
router.get('/map', (req, res) => {
  res.render('map');    // views/map.html
});
router.get('/service', (req, res) => {
  res.render('service'); // views/service.html
});

// FastAPI 호스트 주소
const FASTAPI_HOST = 'http://192.168.1.44:3000';
const forecastAPI = `${FASTAPI_HOST}/r_forecast`;
const recommendAPI = `${FASTAPI_HOST}/ev_recommend`;
const stationAPI = `${FASTAPI_HOST}/r_evstation`;
const stationSidoAPI = `${FASTAPI_HOST}/r_evstation_sido`;

// 🚘 전기차 등록 예측
router.get('/r_forecast', async (req, res) => {
  const { sido, sigungu } = req.query;

  if (!sido || !sigungu) {
    return res.status(400).json({
      result: false,
      message: '❗ 시도명(sido)과 시군구명(sigungu)을 모두 입력해주세요.'
    });
  }

  try {
    const response = await axios.get(forecastAPI, { params: { sido, sigungu } });
    const fastapiData = response.data;
    const { sido: _sido, sigungu: _sigungu, ...forecast } = fastapiData;

    return res.status(200).json({
      result: true,
      data: {
        sido: _sido,
        sigungu: _sigungu,
        forecast
      }
    });

  } catch (error) {
    console.error('[❌ /r_forecast 호출 오류]', error?.response?.data || error.message);
    const status = error.response?.status || 500;
    const message = error.response?.data?.detail || 'FastAPI 예측 데이터 호출 중 오류';
    return res.status(status).json({ result: false, message });
  }
});

// 🔋 전기차 충전소 수 조회
router.get('/r_evstation', async (req, res) => {
  const { sido, sigungu } = req.query;

  if (!sido || !sigungu) {
    return res.status(400).json({
      result: false,
      message: '❗ 시도명(sido)과 시군구명(sigungu)은 필수입니다.'
    });
  }

  try {
    const response = await axios.get(stationAPI, {
      params: { sido, sigungu }
    });

    return res.status(200).json(response.data);

  } catch (error) {
    console.error('[❌ /r_evstation 호출 실패]', error?.response?.data || error.message);
    const status = error.response?.status || 500;
    const message = error.response?.data?.detail || 'FastAPI 충전소 수 API 오류';
    return res.status(status).json({ result: false, message });
  }
});

// 🧭 시도별 충전소 통계 조회
router.get('/r_evstation_sido', async (req, res) => {
  try {
    const response = await axios.get(stationSidoAPI);
    return res.status(200).json(response.data);

  } catch (error) {
    console.error('[❌ /r_evstation_sido 호출 오류]', error?.response?.data || error.message);
    const status = error.response?.status || 500;
    const message = error.response?.data?.detail || 'FastAPI 시도별 충전소 수 호출 실패';
    return res.status(status).json({ result: false, message });
  }
});

// 🔮 전기차 구매 시기 추천
router.get('/ev_recommend', async (req, res) => {
  const { sido, sigungu, year } = req.query;

  if (!sido || !sigungu) {
    return res.status(400).json({
      result: false,
      message: '❗ 시도명(sido)과 시군구명(sigungu)은 필수입니다.'
    });
  }

  try {
    const response = await axios.get(recommendAPI, {
      params: { sido, sigungu, ...(year ? { year } : {}) }
    });

    return res.status(200).json(response.data);

  } catch (error) {
    console.error('[❌ /ev_recommend 호출 오류]', error?.response?.data || error.message);
    const status = error.response?.status || 500;
    const message = error.response?.data?.detail || 'FastAPI 추천 분석 호출 실패';
    return res.status(status).json({ result: false, message });
  }
});

module.exports = router;
