// map.js

// 0) Kakao SDK가 완전히 로드된 후에만 실행되도록 변경
// 기존 window.addEventListener('DOMContentLoaded', ...) 대신 kakao.maps.load을 사용합니다.
kakao.maps.load(initMap);

function initMap() {
  const BASE_URL = 'http://192.168.1.46:3000';

  // 1) 지도 생성
  const map = new kakao.maps.Map(
    document.getElementById('map'),
    {
      center: new kakao.maps.LatLng(37.5665, 126.9780),
      level: 4
    }
  );

  // 2) Geocoder & Places 서비스
  const geocoder = new kakao.maps.services.Geocoder();
  const places   = new kakao.maps.services.Places();

  // 3) 마커 및 인포윈도우 초기화
  let singleMarker = null;
  const stationMarkers = [];
  const infoWindow = new kakao.maps.InfoWindow({ removable: true });
  let lastOpenedMarker = null;

  function setMarker(latLng) {
    if (singleMarker) singleMarker.setMap(null);
    singleMarker = new kakao.maps.Marker({ map, position: latLng });
    map.setCenter(latLng);
  }
  function clearStationMarkers() {
    stationMarkers.forEach(m => m.setMap(null));
    stationMarkers.length = 0;
    if (lastOpenedMarker) {
      infoWindow.close();
      lastOpenedMarker = null;
    }
  }

  // 4) 주변 충전소 조회 함수
  async function fetchStations(lat, lng, rangeKm) {
    clearStationMarkers();
    const listEl = document.getElementById('stationList');
    listEl.innerHTML = '';

    const url = new URL(`${BASE_URL}/r_nearby`);
    url.searchParams.set('latitude',  lat);
    url.searchParams.set('longitude', lng);
    url.searchParams.set('radius',    rangeKm * 1000);

    try {
      const resp = await fetch(url);
      if (!resp.ok) throw new Error(`API 오류 ${resp.status}`);
      const { charging_stations = [] } = await resp.json();

      if (!charging_stations.length) {
        listEl.innerHTML = '<p>🔍 주변 충전소가 없습니다.</p>';
        return;
      }

      charging_stations.forEach(s => {
        const latNum = parseFloat(s.위도),
              lngNum = parseFloat(s.경도);
        const pos    = new kakao.maps.LatLng(latNum, lngNum);
        const marker = new kakao.maps.Marker({ map, position: pos });
        stationMarkers.push(marker);

        const content = `
          <div style="padding:5px; max-width:200px;">
            <strong>${s.충전소명}</strong><br/>
            주소: ${s.주소}<br/>
            충전기 타입: ${s.충전기타입}<br/>
            설치년도: ${s.설치년도 || '정보 없음'}<br/>
            이용자제한: ${s.이용자제한 || '정보 없음'}
          </div>`;

        kakao.maps.event.addListener(marker, 'click', () => {
          if (lastOpenedMarker === marker) {
            infoWindow.close();
            lastOpenedMarker = null;
          } else {
            infoWindow.setContent(content);
            infoWindow.open(map, marker);
            lastOpenedMarker = marker;
          }
        });

        // 사이드바 리스트 아이템
        const item = document.createElement('div');
        item.className = 'station-item';
        item.textContent = s.충전소명;
        item.addEventListener('click', () => {
          map.setCenter(pos);
          if (lastOpenedMarker === marker) {
            infoWindow.close();
            lastOpenedMarker = null;
          } else {
            infoWindow.setContent(content);
            infoWindow.open(map, marker);
            lastOpenedMarker = marker;
          }
        });
        listEl.appendChild(item);
      });
    } catch (err) {
      alert(`충전소 API 호출 실패: ${err.message}`);
    }
  }

  // 5) “현재 위치에서 찾기” 버튼
  document.getElementById('locateBtn').addEventListener('click', () => {
    const lat = 37.4946121541249,
          lng = 127.02757944598672;
    const pos = new kakao.maps.LatLng(lat, lng);
    setMarker(pos);
    const range = parseFloat(document.getElementById('range').value) || 2;
    fetchStations(lat, lng, range);
  });

  // 6) “주소로 찾기” 버튼
  document.getElementById('addressSearchBtn').addEventListener('click', () => {
    const input = document.getElementById('address').value.trim();
    if (!input) return alert('주소를 입력해주세요.');

    geocoder.addressSearch(input, (res, status) => {
      if (status === kakao.maps.services.Status.OK && res[0]) {
        const { y, x } = res[0];
        const p = new kakao.maps.LatLng(y, x);
        setMarker(p);
        const range = parseFloat(document.getElementById('range').value) || 2;
        fetchStations(y, x, range);
      } else {
        places.keywordSearch(input, (data, status2) => {
          if (status2 === kakao.maps.services.Status.OK && data[0]) {
            const { y, x } = data[0];
            const p = new kakao.maps.LatLng(y, x);
            setMarker(p);
            const range = parseFloat(document.getElementById('range').value) || 2;
            fetchStations(y, x, range);
          } else {
            alert('검색 결과가 없습니다.');
          }
        });
      }
    });
  });

  // 7) 경로 기반 충전소 탐색 폼
  document.getElementById('stationForm').addEventListener('submit', async e => {
    e.preventDefault();
    const startAddr = document.getElementById('start').value.trim();
    const rangeKm   = parseFloat(document.getElementById('range').value);
    if (!startAddr || isNaN(rangeKm)) {
      return alert('출발지·도착지·남은 주행거리를 모두 입력하세요.');
    }

    // 주소→좌표 헬퍼
    const geocode = addr => new Promise((resolve, reject) => {
      geocoder.addressSearch(addr, (r, s) => {
        if (s === kakao.maps.services.Status.OK && r[0]) {
          return resolve({ lat: r[0].y, lng: r[0].x });
        }
        places.keywordSearch(addr, (d, s2) => {
          if (s2 === kakao.maps.services.Status.OK && d[0]) {
            return resolve({ lat: d[0].y, lng: d[0].x });
          }
          reject(addr);
        });
      });
    });

    let start;
    try {
      [start] = await Promise.all([startAddr].map(geocode));
    } catch(addr) {
      return alert(`주소 변환 실패: ${addr}`);
    }

    const startPos = new kakao.maps.LatLng(start.lat, start.lng);
    new kakao.maps.Polyline({
      map,
      path: [ startPos ],
      strokeWeight: 4,
      strokeColor: '#2e7d32'
    });
    setMarker(startPos);
    fetchStations(start.lat, start.lng, rangeKm);
  });
}