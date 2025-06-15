const button = document.getElementById("chatbot-button");
const modal = document.getElementById("chatbot-modal");
const close = document.getElementById("chatbot-close");
const chatWindow = document.getElementById("chat-window");
const userInput = document.getElementById("user-input");
const sendButton = document.getElementById("send-button");

let isFirstMessage = true;

button.addEventListener("click", () => {
  modal.style.display = "flex";
  setTimeout(() => userInput.focus(), 300);
});

close.addEventListener("click", () => {
  modal.style.display = "none";
});

// Close modal when clicking outside
modal.addEventListener("click", (e) => {
  if (e.target === modal) {
    modal.style.display = "none";
  }
});

function sendMessage() {
  const userText = userInput.value.trim();
  if (userText === "") return;

  // Clear welcome message on first interaction
  if (isFirstMessage) {
    chatWindow.innerHTML = "";
    isFirstMessage = false;
  }

  // Display user's message
  appendMessage("user", userText);
  userInput.value = "";

  // Show thinking indicator
  const thinkingElement = showThinking();

  // Simulate API call (replace with your actual fetch call)
  setTimeout(async () => {
    try {
      // Replace this with your actual API call
      const response = await fetch("/chat", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({ message: userText }),
      });

      if (!response.ok) {
        throw new Error("Failed to get response from server.");
      }

      const data = await response.json();

      // Remove thinking indicator
      thinkingElement.remove();

      // Display bot response
      appendMessage("bot", data.response);
    } catch (error) {
      console.error("Chat Error:", error);
      thinkingElement.remove();
      appendMessage(
        "bot",
        "Sorry, I encountered an issue. Please try again! 🌾"
      );
    }
  }, 1000); // Simulate network delay
}

userInput.addEventListener("keypress", function (e) {
  if (e.key === "Enter") {
    sendMessage();
  }
});

sendButton.addEventListener("click", sendMessage);

function appendMessage(sender, text) {
  const messageDiv = document.createElement("div");
  messageDiv.className = `message ${sender}`;

  const avatar = document.createElement("div");
  avatar.className = "message-avatar";
  avatar.innerHTML =
    sender === "bot"
      ? '<i class="fas fa-seedling"></i>'
      : '<i class="fas fa-user"></i>';

  const content = document.createElement("div");
  content.className = "message-content";
  content.textContent = text;

  messageDiv.appendChild(avatar);
  messageDiv.appendChild(content);
  chatWindow.appendChild(messageDiv);

  // Smooth scroll to bottom
  chatWindow.scrollTo({
    top: chatWindow.scrollHeight,
    behavior: "smooth",
  });
}

function showThinking() {
  const messageDiv = document.createElement("div");
  messageDiv.className = "message bot";

  const avatar = document.createElement("div");
  avatar.className = "message-avatar";
  avatar.innerHTML = '<i class="fas fa-seedling"></i>';

  const content = document.createElement("div");
  content.className = "message-content";
  content.innerHTML = `
                <div class="thinking-dots">
                    <span></span>
                    <span></span>
                    <span></span>
                </div>
            `;

  messageDiv.appendChild(avatar);
  messageDiv.appendChild(content);
  chatWindow.appendChild(messageDiv);

  chatWindow.scrollTo({
    top: chatWindow.scrollHeight,
    behavior: "smooth",
  });

  return messageDiv;
}
