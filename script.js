document.getElementById('send-btn').addEventListener('click', function() {
    const userInput = document.getElementById('user-input');
    const messages = document.getElementById('messages');

    if (userInput.value.trim() !== '') {
        // Add user's message
        const userMessage = document.createElement('p');
        userMessage.textContent = `Tú: ${userInput.value}`;
        userMessage.style.margin = '5px 0';
        messages.appendChild(userMessage);

        // Add chatbot's response
        const botMessage = document.createElement('p');

        //En teoria aqui tendriamos que hacer la llamada a la API de OpenAI, pero por ahora solo vamos a simular una respuesta
        botMessage.textContent = 'Chatbot: ¡Hola! ¿Cómo puedo ayudarte?';
        botMessage.style.margin = '5px 0';
        botMessage.style.color = '#888';
        messages.appendChild(botMessage);

        // Clear input
        userInput.value = '';

        // Scroll to the bottom
        messages.scrollTop = messages.scrollHeight;
    }
});