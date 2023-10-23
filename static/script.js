textInput = $("#textInput")

function getBotResponse() {
    const rawText = textInput.val();

    // Add user input to conversation
    let userMessage = document.createElement('div');
    userMessage.classList.add('chatbot-message', 'user-message')
    userMessage.innerHTML = '<p class="chatbot-text user-message-color">' + rawText + "</p>";
    $("#chatbox").append(userMessage);
    document
        .getElementById("userInput")
        .scrollIntoView({block: "start", behavior: "smooth"});

    // Clear input field
    textInput.val("");


    // Call api to generate bot message
    $.get("/get", {msg: rawText}).done(function (data) {
        // Add bot message to conversation
        let botMessage = document.createElement('div')
        botMessage.classList.add('chatbot-message', 'bot-message')
        botMessage.innerHTML = '<p class="chatbot-text bot-message-color">' + data + "</p>";
        $("#chatbox").append(botMessage);
        document
            .getElementById("userInput")
            .scrollIntoView({block: "start", behavior: "smooth"});
    });
}

textInput.keypress(function (e) {
    if (e.which === 13) {
        getBotResponse();
    }
});