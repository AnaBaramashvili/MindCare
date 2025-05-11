document.addEventListener("DOMContentLoaded", function () {
    const ctx = document.getElementById('healthChart').getContext('2d');
  
    new Chart(ctx, {
      type: 'line',
      data: {
        labels: window.chartData.labels,
        datasets: [{
          label: 'Mental Health Score',
          data: window.chartData.scores,
          borderColor: '#0d6efd',
          backgroundColor: 'rgba(13, 110, 253, 0.1)',
          fill: 'start',
          tension: 0.4,
          pointRadius: 4,
          pointHoverRadius: 6
        }]
      },
      options: {
        responsive: true,
        maintainAspectRatio: false,
        scales: {
          y: {
            beginAtZero: true,
            suggestedMax: 100,
            ticks: { stepSize: 20 }
          }
        },
        plugins: {
          legend: {
            display: true,
            labels: {
              color: '#444',
              font: { weight: 'bold' }
            }
          }
        }
      }
    });
  });
  