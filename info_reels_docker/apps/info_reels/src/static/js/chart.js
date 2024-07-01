let cpuChart, hddChart, memChart;

function fetchUsageData() {
  fetch('/dashboard')
    .then(response => response.json())
    .then(data => {
          // CPU 차트 업데이트
              if (cpuChart) {
                cpuChart.data.datasets[0].data = [data.cpu_usage, 100 - data.cpu_usage];
                cpuChart.data['labels']=[`CPU 사용량 ${data.cpu_usage}%`, `여유 공간 ${100 - data.cpu_usage}%`];
                cpuChart.update();
              } else {
                cpuChart = new Chart(document.getElementById('cpuChart'), {
                  type: 'doughnut',
                  data: {
                    labels: [`CPU 사용량 ${data.cpu_usage}%`, `여유 공간 ${100 - data.cpu_usage}%`],
                    datasets: [{
                      label: 'CPU 사용량',
                      data: [data.cpu_usage, 100 - data.cpu_usage],
                      backgroundColor: ['#FF6384', '#E0E0E0']
                    }]
                  },
                  options: {
                    responsive: true,
                    maintainAspectRatio: false
                  }
                });
              }
              if (hddChart) {
          hddChart.data.datasets[0].data = [data.hdd_usage, 100 - data.hdd_usage];
          hddChart.data['labels'] = [`HDD 사용량 ${data.hdd_usage}%`, `여유 공간 ${100 - data.hdd_usage}%`];
          hddChart.update();
        } else {
          hddChart = new Chart(document.getElementById('hddChart'), {
            type: 'doughnut',
            data: {
              labels: [`HDD 사용량 ${data.hdd_usage}%`, `여유 공간 ${100 - data.hdd_usage}%`],
              datasets: [{
                label: 'HDD 사용량',
                data: [data.hdd_usage, 100 - data.hdd_usage],
                backgroundColor: ['#36A2EB', '#E0E0E0']
              }]
            },
            options: {
              responsive: true,
              maintainAspectRatio: false
            }
          });
        }

        // 메모리(MEM) 차트 업데이트
        if (memChart) {
          memChart.data.datasets[0].data = [data.mem_usage, 100 - data.mem_usage];
          memChart.data['labels'] = [`MEM 사용량 ${data.mem_usage}%`, `여유 공간 ${100 - data.mem_usage}%`];
          memChart.update();
        } else {
          memChart = new Chart(document.getElementById('memChart'), {
            type: 'doughnut',
            data: {
              labels: [`MEM 사용량 ${data.mem_usage}%`, `여유 공간 ${100 - data.mem_usage}%`],
              datasets: [{
                label: 'MEM 사용량',
                data: [data.mem_usage, 100 - data.mem_usage],
                backgroundColor: ['#FFCE56', '#E0E0E0']
              }]
            },
            options: {
              responsive: true,
              maintainAspectRatio: false
            }
          });
        }

    })
    .catch(error => console.error('Error fetching usage data:', error));
}

// 30초마다 자원 사용량 데이터 가져오기
setInterval(fetchUsageData, 3000);

// 초기 실행
fetchUsageData();
