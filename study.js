// Sample flashcards (question:answer)
let flashcards = [
  { question: "What is the capital of France?", answer: "Paris" },
  { question: "What is 2 + 2?", answer: "4" },
  { question: "What color is the sky?", answer: "Blue" }
];

let remainingCards = [];
let currentCard = null;
let correct = 0;
let incorrect = 0;

document.addEventListener("DOMContentLoaded", () => {
  document.getElementById("loadBtn").addEventListener("click", loadFlashcards);
  document.getElementById("nextBtn").addEventListener("click", nextCard);
  document.getElementById("checkBtn").addEventListener("click", checkAnswer);
});

function loadFlashcards() {
  remainingCards = [...flashcards];
  shuffleArray(remainingCards);
  correct = 0;
  incorrect = 0;
  nextCard();
}

function nextCard() {
  const questionLabel = document.getElementById("questionLabel");
  const answerInput = document.getElementById("answerInput");
  const output = document.getElementById("outputArea");

  if (remainingCards.length === 0) {
    questionLabel.textContent = "";
    output.value = `Quiz complete!\nCorrect: ${correct} | Incorrect: ${incorrect}`;
    return;
  }

  currentCard = remainingCards.pop();
  questionLabel.textContent = currentCard.question;
  answerInput.value = "";
  output.value = "";
}

function checkAnswer() {
  const answerInput = document.getElementById("answerInput");
  const output = document.getElementById("outputArea");

  if (!currentCard) {
    output.value = "No card selected.";
    return;
  }

  const userAnswer = answerInput.value.trim().toLowerCase();
  const correctAnswer = currentCard.answer.trim().toLowerCase();

  if (userAnswer === correctAnswer) {
    correct++;
    output.value = "Correct!";
  } else {
    incorrect++;
    output.value = `Incorrect. The correct answer was: ${currentCard.answer}`;
  }

  output.value += `\nCorrect: ${correct} | Incorrect: ${incorrect}`;
}

function shuffleArray(array) {
  for (let i = array.length - 1; i > 0; i--) {
    const j = Math.floor(Math.random() * (i + 1));
    [array[i], array[j]] = [array[j], array[i]];
  }
}

document.addEventListener("DOMContentLoaded", () => {
  // Button and body references
  const toggleBtn = document.getElementById("toggleMode");
  const body = document.body;

  // Load and apply saved theme
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
});

