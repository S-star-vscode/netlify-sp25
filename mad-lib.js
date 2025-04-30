const storyTemplates = {
    "Fox Story": {
      template: "The {adj1} fox jumped over the {adj2} dog.",
      placeholders: ["adj1", "adj2"]
    },
    "Adventure Story": {
      template: "One day, a {adj1} explorer found a {noun1} in the {place}.",
      placeholders: ["adj1", "noun1", "place"]
    },
    "Sci-Fi Story": {
      template: "In the year {year}, a {adj1} robot named {name} saved {planet} from disaster.",
      placeholders: ["year", "adj1", "name", "planet"]
    }
  };
  
  const storySelect = document.getElementById("storySelect");
  const inputContainer = document.getElementById("inputContainer");
  const generateBtn = document.getElementById("generateBtn");
  const output = document.getElementById("output");
  
  // Create and insert Clear button
  const clearBtn = document.createElement("button");
  clearBtn.textContent = "Clear";
  clearBtn.id = "clearBtn";
  document.getElementById("buttonContainer")?.appendChild(clearBtn) || generateBtn.insertAdjacentElement("afterend", clearBtn);
  
  storySelect.addEventListener("change", () => {
    inputContainer.innerHTML = "";
    const selectedStory = storyTemplates[storySelect.value];
  
    if (selectedStory) {
      selectedStory.placeholders.forEach((placeholder) => {
        const group = document.createElement("div");
        group.className = "input-group";
        const label = document.createElement("label");
        label.textContent = `Enter ${placeholder}:`;
        const input = document.createElement("input");
        input.type = "text";
        input.id = placeholder;
        group.appendChild(label);
        group.appendChild(input);
        inputContainer.appendChild(group);
      });
    }
  });
  
  generateBtn.addEventListener("click", () => {
    const selectedStory = storyTemplates[storySelect.value];
    if (!selectedStory) {
      output.textContent = "Please select a story.";
      return;
    }
  
    const values = {};
    let allFilled = true;
  
    selectedStory.placeholders.forEach((placeholder) => {
      const input = document.getElementById(placeholder);
      const value = input.value.trim();
      if (!value) {
        allFilled = false;
      }
      values[placeholder] = value;
    });
  
    if (!allFilled) {
      output.textContent = "Please fill in all blanks.";
      return;
    }
  
    let finalStory = selectedStory.template;
    for (let key in values) {
      finalStory = finalStory.replace(`{${key}}`, values[key]);
    }
  
    output.textContent = finalStory;
  });
  
  // Clear button functionality
  clearBtn.addEventListener("click", () => {
    inputContainer.innerHTML = "";
    output.textContent = "";
    storySelect.selectedIndex = 0;
  });
  

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