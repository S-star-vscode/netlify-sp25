document.addEventListener("DOMContentLoaded", () => {
    const fileTable = document.getElementById("fileTable").querySelector("tbody");
    const toggleBtn = document.getElementById("toggleTheme");
    const body = document.body;

    const files = [
      { name: "report.txt", size: "14 KB", modified: "2025-04-30 09:12" },
      { name: "image.jpg", size: "1.2 MB", modified: "2025-04-28 13:47" },
      { name: "archive.zip", size: "5.4 MB", modified: "2025-04-25 18:10" },
      { name: "script.py", size: "3 KB", modified: "2025-04-29 21:34" }
    ];

    let currentSort = { column: null, ascending: true };

    function renderTable(data) {
      fileTable.innerHTML = "";
      data.forEach((file, index) => {
        const row = document.createElement("tr");
        row.innerHTML = `
          <td><input type="checkbox" data-index="${index}" /> ${file.name}</td>
          <td>${file.size}</td>
          <td>${file.modified}</td>
        `;
        fileTable.appendChild(row);
      });
    }

    function sortFiles(column) {
      const key = column.dataset.sort;
      if (currentSort.column === key) {
        currentSort.ascending = !currentSort.ascending;
      } else {
        currentSort = { column: key, ascending: true };
      }

      files.sort((a, b) => {
        if (key === "size") {
          return getSizeValue(a.size) - getSizeValue(b.size);
        } else if (key === "modified") {
          return new Date(a.modified) - new Date(b.modified);
        } else {
          return a.name.localeCompare(b.name);
        }
      });

      if (!currentSort.ascending) files.reverse();
      renderTable(files);
    }

    function getSizeValue(sizeStr) {
      const [value, unit] = sizeStr.split(" ");
      const size = parseFloat(value);
      if (unit === "KB") return size * 1024;
      if (unit === "MB") return size * 1024 * 1024;
      return size;
    }

    // Theme loading and toggle
    const savedTheme = localStorage.getItem("theme") || "light";
    body.classList.add(savedTheme);
    updateToggleText(savedTheme);

    toggleBtn.addEventListener("click", () => {
      const current = body.classList.contains("dark") ? "dark" : "light";
      const newTheme = current === "dark" ? "light" : "dark";
      body.classList.replace(current, newTheme);
      localStorage.setItem("theme", newTheme);
      updateToggleText(newTheme);
    });

    function updateToggleText(theme) {
      toggleBtn.textContent = theme === "dark" ? "🌞 Toggle Light Mode" : "🌙 Toggle Dark Mode";
    }

    // Initial render
    renderTable(files);

    // Sort handlers
    document.querySelectorAll("th").forEach(th => {
      th.addEventListener("click", () => sortFiles(th));
    });

    document.getElementById("moveBtn").addEventListener("click", () =>
      alert("Move operation not implemented in browser!")
    );

    document.getElementById("deleteBtn").addEventListener("click", () => {
      const checkboxes = document.querySelectorAll("#fileTable tbody input[type='checkbox']");
      const toDelete = [];

      checkboxes.forEach(cb => {
        if (cb.checked) {
          const index = parseInt(cb.dataset.index);
          toDelete.push(index);
        }
      });

      if (toDelete.length === 0) {
        alert("No files selected for deletion.");
        return;
      }

      toDelete.sort((a, b) => b - a);
      toDelete.forEach(index => files.splice(index, 1));
      renderTable(files);
      alert(`${toDelete.length} file(s) deleted.`);
    });

    document.getElementById("organizeExt").addEventListener("click", () =>
      alert("Organize by Extension clicked")
    );
    document.getElementById("organizeDate").addEventListener("click", () =>
      alert("Organize by Date clicked")
    );
    document.getElementById("organizeSize").addEventListener("click", () =>
      alert("Organize by Size clicked")
    );
    document.getElementById("startWatch").addEventListener("click", () =>
      alert("Start Watching (mock)")
    );
    document.getElementById("stopWatch").addEventListener("click", () =>
      alert("Stop Watching (mock)")
    );
  });