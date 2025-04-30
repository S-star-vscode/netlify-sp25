const toggleBtn = document.getElementById("toggleTheme");
const body = document.body;

// Apply saved theme on page load
window.addEventListener("DOMContentLoaded", () => {
  const savedTheme = localStorage.getItem("theme") || "light";
  body.classList.add(savedTheme);
  updateToggleButton(savedTheme);
});

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
