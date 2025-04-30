function format(command) {
    document.execCommand(command, false, null);
  }
  
  function removeFormatting() {
    const selection = window.getSelection();
    if (!selection.rangeCount) return;
    const range = selection.getRangeAt(0);
    const span = document.createElement("span");
    span.innerHTML = range.toString();
    range.deleteContents();
    range.insertNode(span);
  }
  
  function getDateKey() {
    const dateInput = document.getElementById("journal-date");
    if (!dateInput.value) {
      alert("Please select a date.");
      return null;
    }
    return `entry-${dateInput.value}`;
  }
  
  function saveEntry() {
    const key = getDateKey();
    if (!key) return;
    const content = document.getElementById("editor").innerHTML;
    localStorage.setItem(key, content);
    alert("Entry saved successfully.");
  }
  
  function loadEntry() {
    const key = getDateKey();
    if (!key) return;
    const content = localStorage.getItem(key);
    if (content !== null) {
      document.getElementById("editor").innerHTML = content;
    } else {
      alert("No entry found for this date.");
      document.getElementById("editor").innerHTML = "";
    }
  }
  
  function searchByTag() {
    const tag = document.getElementById("tag-search").value.trim();
    const resultsList = document.getElementById("search-results");
    resultsList.innerHTML = "";
  
    if (!tag.startsWith("#")) {
      alert("Tags should start with '#'.");
      return;
    }
  
    for (let i = 0; i < localStorage.length; i++) {
      const key = localStorage.key(i);
      if (key.startsWith("entry-")) {
        const content = localStorage.getItem(key);
        if (content.includes(tag)) {
          const li = document.createElement("li");
          li.textContent = `${key.replace("entry-", "")} - contains ${tag}`;
          resultsList.appendChild(li);
        }
      }
    }
}
// Theme toggle logic
window.addEventListener("DOMContentLoaded", () => {
    const body = document.body;
    const toggleBtn = document.getElementById("toggleTheme");
  
    // Apply saved theme or default to light
    const savedTheme = localStorage.getItem("theme") || "light";
    body.classList.add(savedTheme);
    updateToggleButton(savedTheme);
  
    // Toggle theme on click
    toggleBtn.addEventListener("click", () => {
      const currentTheme = body.classList.contains("dark") ? "dark" : "light";
      const newTheme = currentTheme === "dark" ? "light" : "dark";
  
      body.classList.replace(currentTheme, newTheme);
      localStorage.setItem("theme", newTheme);
      updateToggleButton(newTheme);
    });
  
    function updateToggleButton(theme) {
      toggleBtn.innerHTML =
        theme === "dark" ? "🌞 Toggle Light Mode" : "🌙 Toggle Dark Mode";
    }
  });
  
