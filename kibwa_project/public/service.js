document.addEventListener("DOMContentLoaded", () => {
  const sidoInput = document.getElementById("sido");
  const sigunguInput = document.getElementById("sigungu");
  const yearInput = document.getElementById("year");
  const resultBox = document.querySelector(".result-box");
  const button = document.getElementById("recommendBtn");

  button.addEventListener("click", async () => {
    const sido = sidoInput.value.trim();
    const sigungu = sigunguInput.value.trim();
    const year = yearInput ? yearInput.value.trim() : "";

    if (!sido || !sigungu) {
      resultBox.innerHTML = `<p class="warning">⚠️ 시도명과 시군구명을 모두 입력해주세요.</p>`;
      return;
    }

    resultBox.innerHTML = `<p class="loading">📡 데이터를 불러오는 중...</p>`;

    try {
      const query = `/ev_recommend?sido=${encodeURIComponent(sido)}&sigungu=${encodeURIComponent(sigungu)}${year ? `&year=${year}` : ''}`;
      const response = await fetch(query);
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

      html += `<table class="result-table"><thead><tr><th>연도</th><th>등록대수</th></tr></thead><tbody>`;
      Object.entries(forecast || {})
        .sort(([a], [b]) => a - b)
        .forEach(([year, value]) => {
          const val = parseFloat(value);
          html += `<tr><td>${year}</td><td>${!isNaN(val) ? val.toLocaleString() + " 대" : "정보 없음"}</td></tr>`;
        });
      html += `</tbody></table>`;

      html += `<p class="highlight">✅ 추천 시점: <strong>${recommendation_year ?? '정보 없음'}년</strong></p>`;
      html += `<p class="highlight">💡 ${recommendation ?? '추천 이유 없음'}</p>`;

      resultBox.innerHTML = html;

    } catch (err) {
      console.error(err);
      resultBox.innerHTML = `<p class="error">❗ 서버 오류: ${err.message}</p>`;
    }
  });
});
