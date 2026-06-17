/* ============================================================
   FinTrack — Dashboard: Chart.js doughnut for category breakdown
   ============================================================ */

(function () {
  var canvas = document.getElementById('graficaGastos');
  if (!canvas) return;

  var labels, values;
  try {
    labels = JSON.parse(canvas.dataset.labels || '[]');
    values = JSON.parse(canvas.dataset.values || '[]');
  } catch (e) {
    return;
  }
  if (!labels.length || !values.length) return;

  var ctx = canvas.getContext('2d');
  new Chart(ctx, {
    type: 'doughnut',
    data: {
      labels: labels,
      datasets: [{
        data: values,
        backgroundColor: ['#1a1a2e', '#16213e', '#0f3460', '#533483', '#e94560', '#f5a623'],
        borderWidth: 3,
        borderColor: '#fff',
      }]
    },
    options: {
      responsive: true,
      cutout: '70%',
      plugins: {
        legend: {
          position: 'bottom',
          labels: {
            padding: 16,
            usePointStyle: true,
            pointStyleWidth: 12,
            font: { size: 12 }
          }
        },
        tooltip: {
          backgroundColor: '#1a1a2e',
          titleFont: { size: 13 },
          bodyFont: { size: 12 },
          padding: 12,
          cornerRadius: 8,
          callbacks: {
            label: function (context) {
              var value = context.parsed;
              var total = context.dataset.data.reduce(function (a, b) { return a + b; }, 0);
              var pct = ((value / total) * 100).toFixed(1);
              return context.label + ': $' + value.toLocaleString('es-CO') + ' COP (' + pct + '%)';
            }
          }
        }
      }
    }
  });
})();
