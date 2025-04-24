const express = require('express');
const axios   = require('axios');
const router  = express.Router();

// 1) 내 FastAPI (예측·추천) 주소
const LOCAL_API_HOST  = 'http://192.168.1.44:3000';

// 2) 상대방 FastAPI (충전소) 주소
const REMOTE_API_HOST = 'http://192.168.1.46:3000';

// 내 FastAPI 용 엔드포인트
const forecastAPI    = `${LOCAL_API_HOST}/r_forecast`;
const recommendAPI   = `${LOCAL_API_HOST}/ev_recommend`;

// 상대방 FastAPI 용 엔드포인트
const stationByAddrAPI = `${REMOTE_API_HOST}/r_by_address`;
const stationNearbyAPI = `${REMOTE_API_HOST}/r_nearby`;
const stationDetailAPI = `${REMOTE_API_HOST}/r_detail`;
const stationRouteAPI  = `${REMOTE_API_HOST}/r_route`;

// 정적 페이지 라우팅
router.get('/',         (req, res) => res.render('index'));
router.get('/analysis', (req, res) => res.render('analysis'));
router.get('/map',      (req, res) => res.render('map'));
router.get('/service',  (req, res) => res.render('service'));

// 🚘 전기차 등록 예측 (내 FastAPI)
router.get('/r_forecast', async (req, res) => {
  const { sido, sigungu } = req.query;
  if (!sido || !sigungu)
    return res.status(400).json({ result: false, message: '시도와 시군구를 모두 입력해주세요.' });

  try {
    const { data } = await axios.get(forecastAPI, { params: { sido, sigungu } });
    res.json({ result: true, data });
  } catch (err) {
    res.status(err.response?.status || 500)
       .json({ result: false, message: err.response?.data?.detail || err.message });
  }
});

// 🔮 전기차 구매 추천 (내 FastAPI)
router.get('/ev_recommend', async (req, res) => {
  const { sido, sigungu, year } = req.query;
  if (!sido || !sigungu)
    return res.status(400).json({ result: false, message: '시도와 시군구를 모두 입력해주세요.' });

  try {
    const { data } = await axios.get(recommendAPI, { params: { sido, sigungu, year } });
    res.json(data);
  } catch (err) {
    res.status(err.response?.status || 500)
       .json({ result: false, message: err.response?.data?.detail || err.message });
  }
});

// 📍 주소 기반 충전소 조회 (상대방 FastAPI)
router.get('/r_by_address', async (req, res) => {
  const { address, radius } = req.query;
  if (!address)
    return res.status(400).json({ result: false, message: '주소를 입력해주세요.' });

  try {
    const { data } = await axios.get(stationByAddrAPI, { params: { address, radius } });
    res.json(data);
  } catch (err) {
    res.status(err.response?.status || 500)
       .json({ result: false, message: err.response?.data?.detail || err.message });
  }
});

// 📍 현재 위치 기반 충전소 조회 (상대방 FastAPI)
router.get('/r_nearby', async (req, res) => {
  const { latitude, longitude, radius } = req.query;
  if (!latitude || !longitude)
    return res.status(400).json({ result: false, message: '위도와 경도를 모두 입력해주세요.' });

  try {
    const { data } = await axios.get(stationNearbyAPI, { params: { latitude, longitude, radius } });
    res.json(data);
  } catch (err) {
    res.status(err.response?.status || 500)
       .json({ result: false, message: err.response?.data?.detail || err.message });
  }
});

// 🧾 충전소 상세정보 조회 (상대방 FastAPI)
router.get('/r_detail', async (req, res) => {
  const { latitude, longitude } = req.query;
  if (!latitude || !longitude)
    return res.status(400).json({ result: false, message: '위도와 경도를 모두 입력해주세요.' });

  try {
    const { data } = await axios.get(stationDetailAPI, { params: { latitude, longitude } });
    res.json(data);
  } catch (err) {
    res.status(err.response?.status || 500)
       .json({ result: false, message: err.response?.data?.detail || err.message });
  }
});

// 🚗 경로 기반 충전소 조회 (상대방 FastAPI)
router.get('/r_route', async (req, res) => {
  const { start_address, end_address, range } = req.query;
  if (!start_address || !end_address || !range)
    return res.status(400).json({ result: false, message: '출발지, 도착지, 주행 가능 거리를 모두 입력해주세요.' });

  try {
    const { data } = await axios.get(stationRouteAPI, {
      params: { start_address, end_address, range }
    });
    res.json(data);
  } catch (err) {
    res.status(err.response?.status || 500)
       .json({ result: false, message: err.response?.data?.detail || err.message });
  }
});

module.exports = router;
