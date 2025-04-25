// 1) 공통 데이터 정의
const labels = [
    '서울', '부산', '대구', '인천', '광주', '대전', '울산', '세종',
    '경기', '강원', '충청', '전라', '경상', '제주'
  ];
  
  // 충청(충북+충남), 전라(전북+전남), 경상(경북+경남) 합산
  const rawDatasets = [
    { label: '2020-12', data: [23393,5355,12630,5366,3210,4469,2274,1148,20477,4078,3883+5489,3323+5223,7051+6308,21285], backgroundColor: '#78dba3' },
    { label: '2021-12', data: [40564,12375,16185,12820,5194,7701,3166,1859,39958,7946,8194+9991,7365+8708,11240+12606,25571], backgroundColor: '#9575cd' },
    { label: '2022-12', data: [59327,22063,24161,26242,9096,14476,5061,3034,77648,14012,15140+16611,12727+15387,19154+22740,32976], backgroundColor: '#4fc3f7' },
    { label: '2023-12', data: [72937,34643,30396,40397,12538,17889,7838,4393,114117,18236,19972+24130,19795+24200,26776+36225,39418], backgroundColor: '#ffb74d' },
    { label: '2024-07', data: [79548,40368,32631,48073,13820,19933,8883,4905,134741,19611,22759+27979,22494+28386,30810+43013,43117], backgroundColor: '#ff8a65' }
  ];
  
  // 2) 총합 계산 후 정렬 인덱스 생성
  const totals = labels.map((_, i) =>
    rawDatasets.reduce((sum, ds) => sum + ds.data[i], 0)
  );
  const sortedIdx = labels.map((_, i) => i)
                          .sort((a, b) => totals[b] - totals[a]);
  
  // 3) 정렬된 라벨·데이터셋
  const sortedLabels = sortedIdx.map(i => labels[i]);
  const sortedDatasets = rawDatasets.map(ds => ({
    ...ds,
    data: sortedIdx.map(i => ds.data[i])
  }));
  
  // === 4) 스택형 막대 차트 ===
  new Chart(
    document.getElementById('barChart').getContext('2d'),
    {
      type: 'bar',
      data: { labels: sortedLabels, datasets: sortedDatasets },
      options: {
        responsive: true,
        plugins: {
          legend: { position: 'top' },
          title: { display: false }
        },
        scales: {
          x: { stacked: true, ticks: { maxRotation: 0 } },
          y: { stacked: true }
        }
      }
    }
  );
  
  // === 5) 상위 5개 파이 차트 ===
  const last = rawDatasets.find(d => d.label === '2024-07');
  const topArr = labels
    .map((lbl, i) => ({ lbl, val: last.data[i] }))
    .sort((a, b) => b.val - a.val)
    .slice(0, 5);
  new Chart(
    document.getElementById('pieChart').getContext('2d'),
    {
      type: 'pie',
      data: {
        labels: topArr.map(d => d.lbl),
        datasets: [{
          data: topArr.map(d => d.val),
          backgroundColor: ['#78dba3','#9575cd','#4fc3f7','#ffb74d','#ff8a65'],
          borderColor: '#fff',
          borderWidth: 2
        }]
      },
      options: { responsive: true, plugins: { legend: { position: 'top' } } }
    }
  );
  
  // === 6) 하위 5개 파이 차트 ===
  const bottomArr = labels
    .map((lbl, i) => ({ lbl, val: last.data[i] }))
    .sort((a, b) => a.val - b.val)
    .slice(0, 5);
  new Chart(
    document.getElementById('pieChartBottom').getContext('2d'),
    {
      type: 'pie',
      data: {
        labels: bottomArr.map(d => d.lbl),
        datasets: [{
          data: bottomArr.map(d => d.val),
          backgroundColor: ['#ff8a65','#ffb74d','#4fc3f7','#9575cd','#78dba3'],
          borderColor: '#fff',
          borderWidth: 2
        }]
      },
      options: { responsive: true, plugins: { legend: { position: 'top' } } }
    }
  );
  
  // === 7) 2024-12 지역별 완속·급속 충전소 수 ===
  const stationLabels = ['서울','경기','인천','경상','전라','충청','강원','제주'];
  const slowData       = [56070,20513,102272,11481,41015,32713,79228,6264];
  const fastData       = [ 4545, 1836,  10112, 2337, 6232, 5872,11345,2297];
  new Chart(
    document.getElementById('stationBarChart').getContext('2d'),
    {
      type: 'bar',
      data: {
        labels: stationLabels,
        datasets: [
          { label: '완속', data: slowData, backgroundColor: '#78dba3' },
          { label: '급속', data: fastData, backgroundColor: '#ffb74d' }
        ]
      },
      options: {
        responsive: true,
        plugins: { legend: { position: 'top' } },
        scales: {
          x: { stacked: false, ticks: { maxRotation: 0 } },
          y: { stacked: false, beginAtZero: true }
        }
      }
    }
  );
  
  // === 8) 2024-12 상위 5개 지역 충전소 비율 파이 차트 ===
  const stationTotals = stationLabels.map((_, i) => slowData[i] + fastData[i]);
  const stationTopArr = stationLabels
    .map((lbl, i) => ({ lbl, val: stationTotals[i] }))
    .sort((a, b) => b.val - a.val)
    .slice(0, 5);
  new Chart(
    document.getElementById('stationTopPie').getContext('2d'),
    {
      type: 'pie',
      data: {
        labels: stationTopArr.map(d => d.lbl),
        datasets: [{
          data: stationTopArr.map(d => d.val),
          backgroundColor: ['#78dba3','#9575cd','#4fc3f7','#ffb74d','#ff8a65'],
          borderColor: '#fff',
          borderWidth: 2
        }]
      },
      options: { responsive: true, plugins: { legend: { position: 'top' } } }
    }
  );
  
  // === 9) 2024-12 완속 vs 급속 충전소 비율 파이 차트 ===
  const totalSlow = slowData.reduce((a, b) => a + b, 0);
  const totalFast = fastData.reduce((a, b) => a + b, 0);
  new Chart(
    document.getElementById('speedPie').getContext('2d'),
    {
      type: 'pie',
      data: {
        labels: ['완속', '급속'],
        datasets: [{
          data: [totalSlow, totalFast],
          backgroundColor: ['#78dba3', '#ffb74d'],
          borderColor: '#fff',
          borderWidth: 2
        }]
      },
      options: { responsive: true, plugins: { legend: { position: 'top' } } }
    }
  );
  