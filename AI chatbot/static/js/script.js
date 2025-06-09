$(document).ready(function () {
    var isBotTyping = false;
    var typingInterval;
    var currentIndex = 0; 

    $('#send-button').click(function () {
        if (!isBotTyping) {
            sendMessage();
        } else {
            stopBotResponse(); 
        }
    });

    $('#message-input').keypress(function (event) {
        if (event.which === 13) { 
            event.preventDefault();  
            if (!isBotTyping) {
                sendMessage();
            }
        }
    });

    function sendMessage() {
        var userMessage = $('#message-input').val().trim();
        if (userMessage) {
            $('#chat-body').append('<div class="chat-message user">' + userMessage + '</div>');
            $('#message-input').val("");

            console.log("Sending Message: ", userMessage);

            $('#send-button').html('<i class="bi bi-stop-fill"></i>');
            isBotTyping = true;

            $('#chat-body').scrollTop($('#chat-body')[0].scrollHeight); 

            $.ajax({
                url: '/chat',
                type: 'POST',
                contentType: 'application/json',
                data: JSON.stringify({ "message": userMessage }),
                success: function (response) {
                    let botMessage = response.response.replace(/\n/g, '<br>');
                    let chatBody = $('#chat-body');
                    let typingMessage = $('<div class="chat-message bot"></div>'); 
                    chatBody.append(typingMessage);
                    chatBody.scrollTop(chatBody[0].scrollHeight);

                    currentIndex = 0; 

                    typingInterval = setInterval(function () {
                        if (currentIndex < botMessage.length) {
                            typingMessage.html(botMessage.slice(0, currentIndex + 1)); 
                            currentIndex++;
                            chatBody.scrollTop(chatBody[0].scrollHeight); 
                        } else {
                            clearInterval(typingInterval);
                            isBotTyping = false;
                            $('#send-button').html('<i class="bi bi-send-plus-fill"></i>'); 
                        }
                    }, 20); 
                },
            });
        }
    }

    function stopBotResponse() {
        clearInterval(typingInterval); 

        isBotTyping = false;
        $('#send-button').html('<i class="bi bi-send-plus-fill"></i>'); 
    }
});
