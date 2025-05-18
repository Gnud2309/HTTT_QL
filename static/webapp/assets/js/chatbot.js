$(document).ready(function () {
    // Mở/đóng widget chatbot
    $('#chatbot-toggle').click(function () {
        $('#chatbot-window').toggle();
    });

    $('#chatbot-close').click(function () {
        $('#chatbot-window').hide();
    });

    // Xử lý gửi tin nhắn
    $('#chatbot-send').click(function () {
        sendMessage();
    });

    $('#chatbot-input').keypress(function (e) {
        if (e.which === 13) { // Nhấn Enter
            sendMessage();
        }
    });

    async function sendMessage() {
        let userInput = $('#chatbot-input').val().trim();
        if (!userInput) return;

        let chatbox = $('#chatbot-messages');
        chatbox.append(`<div class='message user'>Bạn: ${userInput}</div>`);
        $('#chatbot-input').val('');
        chatbox.scrollTop(chatbox[0].scrollHeight);

        try {
            let response = await $.ajax({
                url: 'http://127.0.0.1:5001/chat',
                method: 'POST',
                contentType: 'application/json',
                data: JSON.stringify({ message: userInput })
            });

            let botReply = response.reply ? String(response.reply) : 'Xin lỗi, hệ thống đang bảo trì';

            // Định dạng phản hồi
            let formattedReply = botReply
                .replace(/\*\*(.*?)\*\*/g, '<strong>$1</strong>') // In đậm
                .replace(/\n/g, '<br>'); // Xuống dòng

            chatbox.append(`<div class='message bot'>Bot: ${formattedReply}</div>`);
            chatbox.scrollTop(chatbox[0].scrollHeight);
        } catch (error) {
            console.error('Lỗi gửi yêu cầu:', error);
            chatbox.append(`<div class='message bot'>Lỗi: Không thể kết nối đến chatbot</div>`);
            chatbox.scrollTop(chatbox[0].scrollHeight);
        }
    }
});
