const tryAgainBtn = document.getElementById("try-again");
document.addEventListener("DOMContentLoaded", () => {
    const questionData = [
      {
        question: "What is the capital of France?",
        correct: "Paris",
        choices: ["London", "Berlin", "Rome"]
      },
      {
        question: "What is 2 + 2?",
        correct: "4",
        choices: ["3", "5", "22"]
      },
      {
        question: "Which planet is the Red Planet?",
        correct: "Mars",
        choices: ["Venus", "Jupiter", "Saturn"]
      },
      {
        question: "HTML is used for?",
        correct: "Web development",
        choices: ["Painting", "Cooking", "Driving"]
      },
      {
        question: "Which animal barks?",
        correct: "Dog",
        choices: ["Cat", "Fish", "Cow"]
      }
    ];
  
    let current = 0;
    let score = 0;
    let selectedQuestions = [];
    let incorrectAnswers = [];
  
    const questionBox = document.getElementById("question-box");
    const choicesBox = document.getElementById("choices");
    const resultBox = document.getElementById("result");
    const summaryBox = document.getElementById("incorrect-summary");
  
    function shuffle(array) {
      return array.sort(() => Math.random() - 0.5);
    }
  
    function startQuiz() {
      current = 0;
      score = 0;
      incorrectAnswers = [];
      selectedQuestions = shuffle([...questionData]).slice(0, 5);
      summaryBox.innerHTML = "";
      resultBox.innerHTML = "";
      loadQuestion();
    }
  
    function loadQuestion() {
      const q = selectedQuestions[current];
      const answers = shuffle([q.correct, ...q.choices]);
  
      questionBox.textContent = `Q${current + 1}: ${q.question}`;
      choicesBox.innerHTML = "";
  
      answers.forEach(answer => {
        const btn = document.createElement("button");
        btn.textContent = answer;
        btn.onclick = () => checkAnswer(answer, q.correct);
        choicesBox.appendChild(btn);
      });
    }
  
    function checkAnswer(selected, correct) {
      if (selected === correct) {
        score++;
      } else {
        incorrectAnswers.push({
          question: selectedQuestions[current].question,
          correct,
          selected
        });
      }
  
      current++;
      if (current < selectedQuestions.length) {
        loadQuestion();
      } else {
        showResult();
      }
    }
  
    function showResult() {
        questionBox.textContent = "";
        choicesBox.innerHTML = "";
        resultBox.textContent = `Quiz Complete! Your score: ${score} / ${selectedQuestions.length}`;
        tryAgainBtn.style.display = "inline-block"; // 👈 Show the button
      
      if (incorrectAnswers.length > 0) {
        const heading = document.createElement("h3");
        heading.textContent = "Incorrect Answers:";
        summaryBox.appendChild(heading);
  
        incorrectAnswers.forEach(item => {
          const q = document.createElement("div");
          q.innerHTML = `<strong>${item.question}</strong><br>
            <span class="correct">Correct: ${item.correct}</span><br>
            <span class="incorrect">Your Answer: ${item.selected}</span><br><br>`;
          summaryBox.appendChild(q);
        });
      }
    }
  
    startQuiz();
    tryAgainBtn.onclick = startQuiz;
  });  
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
