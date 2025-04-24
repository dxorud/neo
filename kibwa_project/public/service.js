document.addEventListener("DOMContentLoaded", () => {
  const form = document.getElementById("predictForm");
  const sidoInput = document.getElementById("sido");
  const sigunguInput = document.getElementById("sigungu");
  const yearInput = document.getElementById("year");
  const resultBox = document.getElementById("resultBox");

  function normalizeSido(input) {
    const map = {
      "서울": "서울특별시", "부산": "부산광역시", "대구": "대구광역시", "인천": "인천광역시",
      "광주": "광주광역시", "대전": "대전광역시", "울산": "울산광역시", "세종": "세종특별자치시",
      "경기": "경기도", "강원": "강원특별자치도", "충북": "충청북도", "충남": "충청남도",
      "전북": "전라북도", "전남": "전라남도", "경북": "경상북도", "경남": "경상남도",
      "제주": "제주특별자치도"
    };
    return map[input] || input;
  }

  form.addEventListener("submit", async (e) => {
    e.preventDefault();

    const sido = normalizeSido(sidoInput.value.trim());
    const sigungu = sigunguInput.value.trim();
    const year = yearInput.value.trim();
    const currentYear = new Date().getFullYear(); // ✅ 현재 연도 기준

    // 입력 필수 검사
    if (!sido || !sigungu) {
      resultBox.innerHTML = `<p class="warning">⚠️ 시도명과 시군구명을 모두 입력해주세요.</p>`;
      return;
    }

    // 과거 연도 입력 예외 처리
    if (year && parseInt(year) < currentYear) {
      resultBox.innerHTML = `<p class="warning">⚠️ ${currentYear}년 이후의 연도만 예측 가능합니다.</p>`;
      return;
    }

    resultBox.innerHTML = `<p class="loading">📡 데이터를 불러오는 중...</p>`;

    try {
      const query = `http://192.168.1.44:3000/ev_recommend?sido=${encodeURIComponent(sido)}&sigungu=${encodeURIComponent(sigungu)}${year ? `&year=${year}` : ''}`;
      const response = await fetch(query);

      if (response.status === 404) {
        resultBox.innerHTML = `<p class="notfound">❌ 해당 지역의 예측 데이터를 찾을 수 없습니다.<br>정확한 시도/시군구명을 입력해주세요.</p>`;
        return;
      }

      if (!response.ok) throw new Error(`${response.status} 오류`);

      const result = await response.json();
      if (!result.result || !result.data) {
        resultBox.innerHTML = `<p class="notfound">❌ 예측 데이터를 찾을 수 없습니다.</p>`;
        return;
      }

      const {
        sido: _sido,
        sigungu: _sigungu,
        input_year,
        forecast,
        station_count,
        recommendation_year,
        recommendation
      } = result.data;

      let html = `<h3>🚘 ${_sido} ${_sigungu} 전기차 구매 예측 결과</h3>`;
      html += `<p>📅 예측 기준 연도: <strong>${input_year ?? '정보 없음'}</strong></p>`;
      html += `<p>🔌 충전소 수: <strong>${typeof station_count === 'number' ? station_count.toLocaleString() + '개' : '정보 없음'}</strong></p>`;

      // ✅ 연도 등록대수 출력 (중앙 정렬)
      html += `<div class="forecast-list">`;
      html += `<h4>📊 연도 등록대수</h4>`;
      html += `<ul>`;
      Object.entries(forecast || {})
        .sort(([a], [b]) => a - b)
        .forEach(([year, value]) => {
          const val = parseFloat(value);
          html += `<li><span>${year}</span><span>${!isNaN(val) ? val.toLocaleString() + " 대" : "정보 없음"}</span></li>`;
        });
      html += `</ul></div>`;

      html += `<p class="highlight">✅ 추천 시점: <strong>${recommendation_year ?? '정보 없음'}년</strong></p>`;
      html += `<p class="highlight">💡 ${recommendation ?? '추천 이유 없음'}</p>`;

      resultBox.innerHTML = html;

    } catch (err) {
      console.error(err);
      resultBox.innerHTML = `<p class="error">❗ 서버 오류: ${err.message}</p>`;
    }
  });
});
