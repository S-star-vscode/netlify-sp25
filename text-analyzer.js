// Theme toggle functionality
window.addEventListener("DOMContentLoaded", () => {
    const savedTheme = localStorage.getItem("theme") || "light";
    const body = document.body;
    const toggleBtn = document.getElementById("toggleTheme");
  
    body.classList.add(savedTheme);
    updateToggleButton(savedTheme);
  
    toggleBtn.addEventListener("click", () => {
      const currentTheme = body.classList.contains("dark") ? "dark" : "light";
      const newTheme = currentTheme === "dark" ? "light" : "dark";
  
      body.classList.remove(currentTheme);
      body.classList.add(newTheme);
      localStorage.setItem("theme", newTheme);
      updateToggleButton(newTheme);
    });
  
    function updateToggleButton(theme) {
      toggleBtn.innerHTML = theme === "dark"
        ? "🌞 Toggle Light Mode"
        : "🌙 Toggle Dark Mode";
    }
  });
  
  // File processing and chart rendering
  document.getElementById("fileInput").addEventListener("change", function () {
    const file = this.files[0];
    if (file) {
      const reader = new FileReader();
      reader.onload = function (e) {
        const text = e.target.result.toLowerCase();
        const words = text.match(/\b\w+\b/g) || [];
        const wordCount = words.length;
        const wordLengths = words.map(w => w.length);
        const avgLength = wordCount ? (wordLengths.reduce((a, b) => a + b, 0) / wordCount).toFixed(2) : 0;
        const freqMap = {};
        words.forEach(word => freqMap[word] = (freqMap[word] || 0) + 1);
        const sortedWords = Object.entries(freqMap).sort((a, b) => b[1] - a[1]);
        const [mostCommon, frequency] = sortedWords[0] || ["", 0];
  
        document.getElementById("results").innerHTML = `
          <strong>File:</strong> ${file.name}<br />
          <strong>Total Words:</strong> ${wordCount}<br />
          <strong>Most Common Word:</strong> '${mostCommon}' (${frequency} times)<br />
          <strong>Average Word Length:</strong> ${avgLength}
        `;
  
        // Render bar chart of top 5 words
        const topWords = sortedWords.slice(0, 5);
        const labels = topWords.map(item => item[0]);
        const counts = topWords.map(item => item[1]);
  
        const ctx = document.getElementById('chart').getContext('2d');
        if (window.barChart instanceof Chart) {
          window.barChart.destroy();
        }
        window.barChart = new Chart(ctx, {
          type: 'bar',
          data: {
            labels: labels,
            datasets: [{
              label: 'Top 5 Words',
              data: counts,
              backgroundColor: 'rgba(54, 162, 235, 0.6)',
              borderColor: 'rgba(54, 162, 235, 1)',
              borderWidth: 1
            }]
          },
          options: {
            scales: {
              y: {
                beginAtZero: true,
                ticks: {
                  precision: 0
                }
              }
            }
          }
        });
      };
      reader.readAsText(file);
    }
  });
  