// map.js
let map;
let markers = [];

function clearMarkers() {
  markers.forEach(marker => marker.setMap(null));
  markers = [];
}

function addMarkers(stations) {
  clearMarkers();

  if (stations.length > 0) {
    const firstStation = stations[0];
    const firstPosition = new kakao.maps.LatLng(firstStation["위도"], firstStation["경도"]);
    map.setCenter(firstPosition);
  }

  stations.forEach(station => {
    const lat = station["위도"];
    const lon = station["경도"];
    const markerPosition = new kakao.maps.LatLng(lat, lon);

    const marker = new kakao.maps.Marker({
      position: markerPosition,
      title: station["충전소명"]
    });

    kakao.maps.event.addListener(marker, 'click', function () {
      displayStationDetail(station);
    });

    marker.setMap(map);
    markers.push(marker);
  });
}

function displayStationDetail(station) {
  const container = document.getElementById("detailed-info");
  container.innerHTML = `
    <div class="station-detail-item"><strong>충전소명:</strong> ${station["충전소명"]}</div>
    <div class="station-detail-item"><strong>주소:</strong> ${station["주소"]}</div>
    <div class="station-detail-item"><strong>충전기 타입:</strong> ${station["충전기타입"]}</div>
    <div class="station-detail-item"><strong>설치년도:</strong> ${station["설치년도"] ?? '정보 없음'}</div>
    <div class="station-detail-item"><strong>이용자 제한:</strong> ${station["이용자제한"] ?? '제한 없음'}</div>
  `;

  document.getElementById("result").style.display = 'none';
  document.getElementById("station-detail").style.display = 'block';
}

function displayStations(data, method) {
  const container = document.getElementById("result");
  container.style.display = 'block';
  document.getElementById("station-detail").style.display = 'none';

  if (!data.charging_stations || data.charging_stations.length === 0) {
    container.innerHTML = `<p>충전소 데이터를 찾을 수 없습니다.</p>`;
    return;
  }

  container.innerHTML = `
    <p><strong>${method === "address" ? "주소 기반 조회" : "현재 위치 조회"}</strong></p>
    <p>(조회 반경: ${data["반경(m)"]}m)</p>
    <p>총 ${data["충전소 수"]}개 충전소를 찾았습니다.</p>
  `;

  data.charging_stations.forEach(station => {
    container.innerHTML += `
      <div class="station">
        <strong>${station["충전소명"]}</strong><br>
        주소: ${station["주소"]}<br>
        거리: ${station["거리(m)"]}m<br>
        충전기 타입: ${station["충전기타입"]}<br>
        설치년도: ${station["설치년도"] ?? '정보 없음'}<br>
        이용자 제한: ${station["이용자제한"] ?? '제한 없음'}<br>
        <hr>
      </div>
    `;
  });

  addMarkers(data.charging_stations);
}

function getNearbyStations() {
  const lat = 37.4946121541249;
  const lon = 127.02757944598672;
  const radius = 2000;

  fetch(`http://192.168.1.46:3000/r_nearby?latitude=${lat}&longitude=${lon}&radius=${radius}`)
    .then(response => response.json())
    .then(data => displayStations(data, "location"))
    .catch(err => {
      console.error("API 호출 실패", err);
      alert("충전소 데이터를 가져오는 중 오류가 발생했습니다.");
    });
}

function getStationsByAddress() {
  const address = document.getElementById("address").value.trim();
  if (!address) {
    alert("주소를 입력하세요.");
    return;
  }

  const radius = 2000;

  fetch(`http://192.168.1.46:3000/r_by_address?address=${encodeURIComponent(address)}&radius=${radius}`)
    .then(response => response.json())
    .then(data => displayStations(data, "address"))
    .catch(err => {
      console.error("API 호출 실패", err);
      alert("충전소 데이터를 가져오는 중 오류가 발생했습니다.");
    });
}

function showCurrentLocationOnMap() {
  if (navigator.geolocation) {
    navigator.geolocation.getCurrentPosition(position => {
      const lat = position.coords.latitude;
      const lon = position.coords.longitude;

      const locPosition = new kakao.maps.LatLng(lat, lon);

      const marker = new kakao.maps.Marker({
        position: locPosition,
        map: map,
        title: "현재 위치",
        image: new kakao.maps.MarkerImage(
          "https://t1.daumcdn.net/localimg/localimages/07/mapapidoc/markerStar.png",
          new kakao.maps.Size(24, 35)
        )
      });

      const infowindow = new kakao.maps.InfoWindow({
        content: "<div style='padding:5px;'>📍 현재 위치</div>"
      });
      infowindow.open(map, marker);
    });
  }
}

function initMap() {
  const container = document.getElementById('map');
  const options = {
    center: new kakao.maps.LatLng(37.4946121541249, 127.02757944598672),
    level: 4
  };
  map = new kakao.maps.Map(container, options);

  getNearbyStations();
  showCurrentLocationOnMap();
}

window.onload = initMap;
