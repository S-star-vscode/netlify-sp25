function calculate(operator, buttonElement) {
  const num1 = parseFloat(document.getElementById("num1").value);
  const num2 = parseFloat(document.getElementById("num2").value);
  const history = document.getElementById("history");

  // Remove 'selected' class from all operator buttons
  document.querySelectorAll(".buttons button").forEach(btn => btn.classList.remove("selected"));
  // Add 'selected' class to the clicked button
  if (buttonElement) {
    buttonElement.classList.add("selected");
  }

  if (isNaN(num1) || isNaN(num2)) {
    alert("Please enter valid numbers.");
    return;
  }

  let result;
  if (operator === "/" && num2 === 0) {
    alert("Cannot divide by zero.");
    return;
  }

  switch (operator) {
    case "+": result = num1 + num2; break;
    case "-": result = num1 - num2; break;
    case "*": result = num1 * num2; break;
    case "/": result = num1 / num2; break;
  }

  const entry = `${num1} ${operator} ${num2} = ${result}`;
  history.value += entry + "\n";
  history.scrollTop = history.scrollHeight;
}

function saveHistory() {
  const history = document.getElementById("history").value;
  const blob = new Blob([history], { type: "text/plain" });
  const a = document.createElement("a");
  a.href = URL.createObjectURL(blob);
  a.download = "calculator_history.txt";
  a.click();
  URL.revokeObjectURL(a.href);
}

function loadHistory() {
  const input = document.createElement("input");
  input.type = "file";
  input.accept = ".txt";
  input.onchange = event => {
    const file = event.target.files[0];
    if (!file) return;

    const reader = new FileReader();
    reader.onload = e => {
      document.getElementById("history").value = e.target.result;
    };
    reader.readAsText(file);
  };
  input.click();
}
function clearHistory() {
  document.getElementById("history").value = "";
}
const toggleBtn = document.getElementById("toggleTheme");
const body = document.body;

toggleBtn.addEventListener("click", () => {
  body.classList.toggle("dark");
  body.classList.toggle("light");

  toggleBtn.innerHTML = body.classList.contains("dark")
    ? "🌞 Toggle Light Mode"
    : "🌙 Toggle Dark Mode";
});
