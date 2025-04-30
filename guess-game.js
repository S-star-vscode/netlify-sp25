const wordList = ["roof", "window", "closet", "chimney", "kitchen", "basement"];
let secretWord = wordList[Math.floor(Math.random() * wordList.length)];
let maskedWord = Array(secretWord.length).fill("_");
let tries = 6;
let guessedLetters = [];

const maskedWordEl = document.getElementById("maskedWord");
const triesLeftEl = document.getElementById("triesLeft");
const messageEl = document.getElementById("message");

function updateDisplay() {
  maskedWordEl.textContent = maskedWord.join(" ");
  triesLeftEl.textContent = `Tries left: ${tries}`;
}

function makeGuess() {
  const input = document.getElementById("guessInput");
  const guess = input.value.toLowerCase().trim();
  input.value = "";
  messageEl.textContent = "";

  if (!guess) return;

  if (guess.length === 1) {
    if (guessedLetters.includes(guess)) {
      messageEl.textContent = `You've already guessed "${guess}"`;
      return;
    }

    guessedLetters.push(guess);

    if (secretWord.includes(guess)) {
      for (let i = 0; i < secretWord.length; i++) {
        if (secretWord[i] === guess) {
          maskedWord[i] = guess;
        }
      }
    } else {
      tries--;
    }
  } else {
    if (guess === secretWord) {
      maskedWord = secretWord.split("");
    } else {
      tries--;
    }
  }

  updateDisplay();

  if (maskedWord.join("") === secretWord) {
    messageEl.style.color = "green";
    messageEl.textContent = `🎉 You guessed it! "${secretWord.toUpperCase()}"`;
    disableInput();
  } else if (tries <= 0) {
    messageEl.style.color = "red";
    messageEl.textContent = `💀 Game over. The word was "${secretWord.toUpperCase()}".`;
    disableInput();
  }
}

function disableInput() {
  document.getElementById("guessInput").disabled = true;
}
updateDisplay();
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
