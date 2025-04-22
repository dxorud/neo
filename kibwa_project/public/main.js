document.addEventListener("DOMContentLoaded", () => {
    const sigunguBySido = {
      "서울특별시": ["강남구", "송파구", "용산구", "강서구", "노원구"],
      "부산광역시": ["해운대구", "부산진구", "동래구", "남구"]
    };
  
    const sidoSelect = document.getElementById("sido");
    const sigunguSelect = document.getElementById("sigungu");
    const resultBox = document.querySelector(".result-box");
    const button = document.querySelector(".submit-btn");
  
    // 시군구 목록 동적 로딩
    sidoSelect.addEventListener("change", () => {
      const selectedSido = sidoSelect.value;
      sigunguSelect.innerHTML = "";
  
      if (sigunguBySido[selectedSido]) {
        sigunguSelect.disabled = false;
        sigunguBySido[selectedSido].forEach(gugun => {
          const option = document.createElement("option");
          option.value = gugun;
          option.textContent = gugun;
          sigunguSelect.appendChild(option);
        });
      } else {
        sigunguSelect.disabled = true;
        const defaultOption = document.createElement("option");
        defaultOption.textContent = "-- 먼저 시도를 선택하세요 --";
        sigunguSelect.appendChild(defaultOption);
      }
    });
  
    // 예측 버튼 클릭 이벤트
    button.addEventListener("click", async () => {
      const sido = sidoSelect.value;
      const sigungu = sigunguSelect.value;
  
      if (!sido || !sigungu) {
        resultBox.innerHTML = `<p class="warning">시도와 자치구를 모두 선택해 주세요.</p>`;
        return;
      }
  
      resultBox.innerHTML = `<p class="loading">데이터를 불러오는 중...</p>`;
  
      try {
        const response = await fetch(`/api/forecast?sido=${encodeURIComponent(sido)}&sigungu=${encodeURIComponent(sigungu)}`);
        if (!response.ok) throw new Error(`${response.status} 오류`);
  
        const data = await response.json();
        const { sido: _sido, sigungu: _sigungu, ...years } = data;
  
        let html = `<h3>${_sido} ${_sigungu} 등록대수 예측</h3>`;
        html += `<table class="result-table"><thead><tr><th>연도</th><th>등록대수</th></tr></thead><tbody>`;
        Object.entries(years).forEach(([year, value]) => {
          html += `<tr><td>${year}</td><td>${parseFloat(value).toLocaleString()} 대</td></tr>`;
        });
        html += `</tbody></table>`;
  
        resultBox.innerHTML = html;
  
      } catch (err) {
        console.error(err);
        resultBox.innerHTML = `<p class="error">서버 오류: ${err.message}</p>`;
      }
    });
  });
  