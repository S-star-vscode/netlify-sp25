let expenses = [];

function addExpense() {
  const amount = parseFloat(document.getElementById('amount').value);
  const category = document.getElementById('category').value.trim();
  const date = document.getElementById('date').value.trim();

  if (isNaN(amount) || !category || !isValidDate(date)) {
    alert("Please enter valid amount, category, and date (MM-DD-YYYY).");
    return;
  }

  expenses.push({ amount, category, date });
  updateDisplay();
  clearInputs();
  saveToLocal();
}

function isValidDate(dateStr) {
  const regex = /^(0[1-9]|1[0-2])-([0-2][0-9]|3[01])-\d{4}$/;
  return regex.test(dateStr);
}

function updateDisplay(filteredDate = null) {
  const expenseList = document.getElementById('expenseList');
  const totalLabel = document.getElementById('total');
  expenseList.innerHTML = '';

  let total = 0;
  let filteredExpenses = expenses;

  if (filteredDate) {
    filteredExpenses = expenses.filter(exp => exp.date === filteredDate);
  }

  filteredExpenses.slice(-10).forEach((exp, index) => {
    const li = document.createElement('li');
    li.textContent = `$${exp.amount.toFixed(2)} | ${exp.category} | ${exp.date}`;

    const removeBtn = document.createElement('button');
    removeBtn.textContent = "Remove Expense";
    removeBtn.style.marginLeft = "10px";
    removeBtn.onclick = () => {
      const fullIndex = expenses.findIndex(e => e.amount === exp.amount && e.category === exp.category && e.date === exp.date);
      if (fullIndex !== -1) {
        expenses.splice(fullIndex, 1);
        updateDisplay(filteredDate);
        saveToLocal();
      }
    };

    li.appendChild(removeBtn);
    expenseList.appendChild(li);
    total += exp.amount;
  });

  totalLabel.textContent = `Total: $${total.toFixed(2)}`;
}

function applyFilter() {
  const filterDate = document.getElementById('filterDate').value.trim();
  if (!isValidDate(filterDate)) {
    alert("Date must be in MM-DD-YYYY format.");
    return;
  }
  updateDisplay(filterDate);
}

function clearFilter() {
  document.getElementById('filterDate').value = '';
  updateDisplay();
}

function clearInputs() {
  document.getElementById('amount').value = '';
  document.getElementById('category').value = '';
  document.getElementById('date').value = '';
}

function exportToExcel() {
  if (expenses.length === 0) {
    alert("No expenses to export.");
    return;
  }

  const worksheet = XLSX.utils.json_to_sheet(expenses);
  const workbook = XLSX.utils.book_new();
  XLSX.utils.book_append_sheet(workbook, worksheet, "Expenses");

  XLSX.writeFile(workbook, "expenses.xlsx");
}

function importFromExcel(event) {
  const file = event.target.files[0];
  if (!file) return;

  const reader = new FileReader();
  reader.onload = function (e) {
    const data = new Uint8Array(e.target.result);
    const workbook = XLSX.read(data, { type: "array" });
    const sheetName = workbook.SheetNames[0];
    const worksheet = workbook.Sheets[sheetName];
    const imported = XLSX.utils.sheet_to_json(worksheet);
    expenses = imported.map(item => ({
      amount: parseFloat(item.amount),
      category: item.category,
      date: item.date
    }));
    updateDisplay();
    saveToLocal();
  };
  reader.readAsArrayBuffer(file);
}

function saveToLocal() {
  localStorage.setItem('expenses', JSON.stringify(expenses));
}

function loadFromLocal() {
  const saved = localStorage.getItem('expenses');
  if (saved) {
    try {
      expenses = JSON.parse(saved);
      updateDisplay();
    } catch (e) {
      console.error("Failed to load from localStorage.", e);
    }
  }
}

document.addEventListener("DOMContentLoaded", () => {
  loadFromLocal();

  const fileInput = document.createElement("input");
  fileInput.type = "file";
  fileInput.accept = ".xlsx";
  fileInput.style.display = "none";
  fileInput.addEventListener("change", importFromExcel);
  document.body.appendChild(fileInput);

  const buttonRow = document.createElement("div");
  buttonRow.style.display = "flex";
  buttonRow.style.gap = "10px";
  buttonRow.style.marginTop = "10px";

  const loadButton = document.createElement("button");
  loadButton.textContent = "Load from Excel";
  loadButton.onclick = () => fileInput.click();
  buttonRow.appendChild(loadButton);

  const exportButton = document.createElement("button");
  exportButton.textContent = "Save as Excel";
  exportButton.onclick = exportToExcel;
  buttonRow.appendChild(exportButton);

  document.querySelector(".container").appendChild(buttonRow);
});

const toggleBtn = document.getElementById("toggleTheme");
const body = document.body;

// Load saved theme on page load
window.addEventListener("DOMContentLoaded", () => {
  const savedTheme = localStorage.getItem("theme") || "light";
  body.classList.add(savedTheme);
  updateToggleText(savedTheme);
});

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