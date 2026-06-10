async function sendTask() {
    const input = document.getElementById("taskInput");
    const chatBox = document.getElementById("chatBox");

    const rawTask = input.value.trim();
    const task = rawTask.toLowerCase();
    if (!task) return;

    // 👤 user message
    chatBox.innerHTML += `<div class="msg user">${task}</div>`;
    input.value = "";

    // 🤔 loading
    const loading = document.createElement("div");
    loading.className = "msg bot";
    loading.innerText = "Thinking... 🤔";
    chatBox.appendChild(loading);

    scrollToBottom();

    try {
        const response = await fetch("/agent", {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify({ task: rawTask })
        });

        const data = await response.json();

        loading.remove();

        // -----------------------------
        // FORMAT TEXT
        // -----------------------------
        const formatText = (text) => {
            if (!text) return "";

            return text
                .replace(/(\d\.)/g, "\n$1")
                .replace(/\*\*/g, "")
                .trim();
        };

        const botDiv = document.createElement("div");
        botDiv.className = "msg bot";

        // -----------------------------
        // IDENTITY RESPONSE
        // -----------------------------
        if (data.reply) {
            botDiv.innerText = data.reply;
            chatBox.appendChild(botDiv);
        }

        // -----------------------------
        // AI RESPONSE
        // -----------------------------
        else {
            const planner = formatText(data.planner);
            const tutor = formatText(data.tutor);
            const motivation = formatText(data.motivation);

            const finalText = `
📌 Planner:
${planner}

📚 Tutor:
${tutor}

🔥 Motivation:
${motivation}
`;

            chatBox.appendChild(botDiv);
            typeWriter(botDiv, finalText, 15);
        }

        scrollToBottom();

    } catch (error) {
        loading.remove();

        chatBox.innerHTML += `
            <div class="msg bot">
                ❌ Error connecting to server
            </div>
        `;
    }
}


// -----------------------------
// TYPEWRITER EFFECT
// -----------------------------
function typeWriter(element, text, speed = 20) {
    let i = 0;
    element.innerHTML = "";

    function typing() {
        if (i < text.length) {
            element.innerHTML += text.charAt(i) === "\n" ? "<br>" : text.charAt(i);
            i++;

            scrollToBottom();
            setTimeout(typing, speed);
        }
    }

    typing();
}



function scrollToBottom() {
    const chatBox = document.getElementById("chatBox");
    chatBox.scrollTop = chatBox.scrollHeight;
}